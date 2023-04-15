from rest_framework import viewsets
from .models import Product, Zakupki, Sales
from .serializers import ProductSerializer, ZakupkiSerializer, SalesSerializer


class ZakupkiViewSet(viewsets.ModelViewSet):
    queryset = Zakupki.objects.all()
    serializer_class = ZakupkiSerializer

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

    def post(self, request, *args, **kwargs):
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


