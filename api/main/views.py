from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Supply, Sale
from .serializers import SupplySerializer, SaleSerializer
from django.db import connection
from django.http import HttpResponse


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def create(self, request, *args, **kwargs):

        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        sale = self.get_object()
        serializer = SaleSerializer(sale)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        sale = self.get_object()
        serializer = SaleSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        sale = self.get_object()
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupplyViewSet(viewsets.ModelViewSet):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer

    def create(self, request, *args, **kwargs):
        serializer = SupplySerializer(data=request.data)
        if serializer.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(f"CALL UpdateSoldAmount({request.query_params.get('sold_amount')}, {request.query_params.get('price')});")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        suppply = self.get_object()
        serializer = SupplySerializer(suppply)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        supply = self.get_object()
        serializer = SupplySerializer(supply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        supply = self.get_object()
        supply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def update_sold_amount(request):
    with connection.cursor() as cursor:
        # Create the UpdateSoldAmount procedure
        cursor.execute("DROP PROCEDURE IF EXISTS UpdateSoldAmount")
        cursor.execute(f"""
            CREATE PROCEDURE UpdateSoldAmount(IN need_amount FLOAT, IN sale_price FLOAT)
            BEGIN
              DECLARE finished INTEGER DEFAULT 0;
              DECLARE curr_barcode VARCHAR(255);
              DECLARE curr_quantity INTEGER;
              DECLARE curr_sold_amount FLOAT;
              DECLARE delta FLOAT;
              DECLARE cur_price FLOAT;
              DECLARE final_sum FLOAT DEFAULT 0;
              DECLARE need_amount_original FLOAT DEFAULT need_amount;

              -- Cursor to fetch rows that meet the criteria
              DECLARE cur CURSOR FOR
                SELECT barcode, quantity, sold_amount, price
                FROM {Supply._meta.db_table}
                WHERE sold_amount < quantity
                ORDER BY datetime ASC;

              -- Handler for 'not found'
              DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

              OPEN cur;

              update_loop: LOOP
                FETCH cur INTO curr_barcode, curr_quantity, curr_sold_amount, cur_price;

                IF finished = 1 THEN
                  LEAVE update_loop;
                END IF;

                SET delta = curr_quantity - curr_sold_amount;
                IF delta <= need_amount THEN
                  SET need_amount = need_amount - delta;
                  SET curr_sold_amount = curr_quantity;
                  SET final_sum = final_sum + (delta * cur_price);
                ELSE
                  SET curr_sold_amount = curr_sold_amount + need_amount;
                  SET final_sum = final_sum + (need_amount * cur_price);
                  SET need_amount = 0;
                  UPDATE {Supply._meta.db_table}
                  SET sold_amount = curr_sold_amount
                  WHERE barcode = curr_barcode;
                  LEAVE update_loop;
                END IF;

                UPDATE {Supply._meta.db_table}
                SET sold_amount = curr_sold_amount
                WHERE barcode = curr_barcode;

              END LOOP update_loop;

              CLOSE cur;

              SELECT final_sum;

              INSERT INTO {Sale._meta.db_table} (barcode, quantity, datetime, price, margin)
              VALUES ('ABC123', need_amount_original, NOW(), sale_price, ROUND(need_amount_original * sale_price - final_sum, 2));

            END;
        """)
        # cursor.execute(f"""
        #     CREATE PROCEDURE UpdateSoldAmount(IN need_amount FLOAT)
        #     BEGIN
        #       DECLARE finished INTEGER DEFAULT 0;
        #       DECLARE curr_barcode VARCHAR(255);
        #       DECLARE curr_quantity INTEGER;
        #       DECLARE curr_sold_amount INTEGER;
        #       DECLARE delta FLOAT;
        #       DECLARE cur_price FLOAT;
        #       DECLARE final_sum FLOAT DEFAULT 0;
        #
        #       -- Cursor to fetch rows that meet the criteria
        #       DECLARE cur CURSOR FOR
        #         SELECT barcode, quantity, sold_amount, price
        #         FROM {Supply._meta.db_table}
        #         WHERE sold_amount < quantity
        #         ORDER BY datetime ASC;
        #
        #       -- Handler for 'not found'
        #       DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
        #
        #       OPEN cur;
        #
        #       update_loop: LOOP
        #         FETCH cur INTO curr_barcode, curr_quantity, curr_sold_amount, cur_price;
        #
        #         IF finished = 1 THEN
        #           LEAVE update_loop;
        #         END IF;
        #
        #         SET delta = curr_quantity - curr_sold_amount;
        #         IF delta <= need_amount THEN
        #           SET need_amount = need_amount - delta;
        #           SET curr_sold_amount = curr_quantity;
        #           SET final_sum = final_sum + (delta * cur_price);
        #         ELSE
        #           SET curr_sold_amount = curr_sold_amount + need_amount;
        #           SET final_sum = final_sum + (need_amount * cur_price);
        #           SET need_amount = 0;
        #           UPDATE {Supply._meta.db_table}
        #           SET sold_amount = curr_sold_amount
        #           WHERE barcode = curr_barcode;
        #           LEAVE update_loop;
        #         END IF;
        #
        #         UPDATE {Supply._meta.db_table}
        #         SET sold_amount = curr_sold_amount
        #         WHERE barcode = curr_barcode;
        #
        #       END LOOP update_loop;
        #
        #       CLOSE cur;
        #
        #       SELECT final_sum;
        #
        #     END;
        # """)
