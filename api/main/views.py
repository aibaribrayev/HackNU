from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Supply, Sale
from .serializers import SupplySerializer, SaleSerializer


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
        sale = self.get_object(pk)
        serializer = SaleSerializer(sale)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        sale = self.get_object(pk)
        serializer = SaleSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        sale = self.get_object(pk)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

