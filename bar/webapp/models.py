from django.db import models

# Create your models here.

from django.db import models

class Product(models.Model):
    # Django automaticamente agrega id si no es especificado
    name = models.CharField(max_length=20)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    purchase_date = models.DateTimeField()
    provider = models.CharField(max_length=50, null=True)

class PurchaseLine(models.Model):
    compra = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

class Sale(models.Model):
    sale_date = models.DateTimeField()
    client = models.CharField(max_length=50, null=True)

class SaleLine(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
