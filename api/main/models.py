from django.db import models

class Product(models.Model):
    user_id = models.IntegerField(primary_key=True)
    product_id = models.IntegerField(primary_key=True)
    price_id = models.IntegerField(null=True)

class Zakupki(models.Model):
    user_id = models.IntegerField(primary_key=True)
    price_id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    sold_amount = models.FloatField()
    bought_amount = models.FloatField()

class Sales(models.Model):
    user_id = models.IntegerField(primary_key=True)
    price_id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    amount_not_connected = models.FloatField()
