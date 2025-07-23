from django.db import models
from admins.models import Admin
from clients.models import Client
import json

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('brigadeiros', 'Brigadeiros'),
        ('coxinhas', 'Coxinhas de Morango'),
        ('tortas', 'Tortas no Pote'),
        ('kits', 'Kits Festa'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='brigadeiros')
    image = models.CharField(max_length=200, blank=True)  # Store image path
    sizes = models.TextField(blank=True)  # JSON string for size options
    prices = models.TextField(blank=True)  # JSON string for price options
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_sizes(self):
        """Return sizes as list"""
        if self.sizes:
            try:
                return json.loads(self.sizes)
            except json.JSONDecodeError:
                return []
        return []

    def set_sizes(self, sizes_list):
        """Set sizes from list"""
        self.sizes = json.dumps(sizes_list)

    def get_prices(self):
        """Return prices as list"""
        if self.prices:
            try:
                return json.loads(self.prices)
            except json.JSONDecodeError:
                return []
        return []

    def set_prices(self, prices_list):
        """Set prices from list"""
        self.prices = json.dumps(prices_list)

    class Meta:
        ordering = ['name']

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('preparing', 'Preparando'),
        ('ready', 'Pronto'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.client.name}"

    class Meta:
        ordering = ['-purchase_date']

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size_selected = models.CharField(max_length=100, blank=True)  # Selected size
    size_index = models.IntegerField(default=0)  # Index of selected size

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class ProductAction(models.Model):
    ACTION_CHOICES = [
        ('create', 'Criado'),
        ('update', 'Atualizado'),
        ('delete', 'Excluído'),
        ('stock_update', 'Estoque Atualizado'),
    ]
    
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action_type} - {self.product.name}"

    class Meta:
        ordering = ['-action_timestamp']