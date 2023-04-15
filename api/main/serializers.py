from rest_framework import serializers
from .models import Product, Zakupki, Sales

class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Zakupki
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
