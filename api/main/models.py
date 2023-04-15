from django.db import models

class Supply(models.Model):
    barcode = models.CharField(max_length=255)
    quantity = models.IntegerField()
    datetime = models.DateTimeField()
    price = models.FloatField()
    sold_amount = models.IntegerField()


class Sale(models.Model):
    barcode = models.CharField(max_length=255)
    quantity = models.IntegerField()
    datetime = models.DateTimeField()
    price = models.FloatField()
    margin = models.FloatField(default=0)
