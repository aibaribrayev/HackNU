from rest_framework import viewsets
from .models import Product, Zakupki, Sales
from .serializers import ProductSerializer, ZakupkiSerializer, SalesSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ZakupkiViewSet(viewsets.ModelViewSet):
    queryset = Zakupki.objects.all()
    serializer_class = ZakupkiSerializer

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
