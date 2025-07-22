from django.db import models
from admins.models import Admin
from clients.models import Client

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)

class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ProductAction(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20)
    action_timestamp = models.DateTimeField(auto_now_add=True)
