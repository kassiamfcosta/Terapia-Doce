# Backend/backend/core/admin.py - Enhanced admin interface
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Purchase, PurchaseItem, ProductAction
import json

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'image_preview', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('Preços e Estoque', {
            'fields': ('price', 'stock')
        }),
        ('Variações de Tamanho', {
            'fields': ('sizes_display', 'prices_display'),
            'description': 'Para editar tamanhos e preços, use os campos abaixo.'
        }),
        ('Configuração Avançada', {
            'fields': ('sizes_json', 'prices_json', 'image'),
            'classes': ('collapse',)
        }),
        ('Informações do Sistema', {
            'fields': ('created_by', 'created_at', 'updated_at', 'image_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 25px;" />', obj.image)
        return "Sem imagem"
    image_preview.short_description = "Preview"
    
    def sizes_display(self, obj):
        sizes = obj.get_sizes()
        if sizes:
            return ', '.join(sizes)
        return "Nenhum tamanho configurado"
    sizes_display.short_description = "Tamanhos Disponíveis"
    
    def prices_display(self, obj):
        prices = obj.get_prices()
        if prices:
            return ', '.join([f'R$ {p:.2f}' for p in prices])
        return "Nenhum preço configurado"
    prices_display.short_description = "Preços por Tamanho"
    
    def sizes_json(self, obj):
        return obj.sizes if obj.sizes else '[]'
    sizes_json.short_description = "Tamanhos (JSON)"
    
    def prices_json(self, obj):
        return obj.prices if obj.prices else '[]'
    prices_json.short_description = "Preços (JSON)"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new product
            # Get or create admin profile for the user
            from admins.models import Admin
            admin_profile, created = Admin.objects.get_or_create(
                user=request.user,
                defaults={
                    'name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'role': 'admin'
                }
            )
            obj.created_by = admin_profile
            
        # Handle JSON fields if they were edited
        sizes_json = form.cleaned_data.get('sizes_json', '')
        if sizes_json:
            try:
                sizes_list = json.loads(sizes_json)
                obj.set_sizes(sizes_list)
            except json.JSONDecodeError:
                pass
        
        prices_json = form.cleaned_data.get('prices_json', '')
        if prices_json:
            try:
                prices_list = json.loads(prices_json)
                obj.set_prices(prices_list)
            except json.JSONDecodeError:
                pass
                
        super().save_model(request, obj, form, change)

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    readonly_fields = ['product', 'quantity', 'price', 'size_selected']
    extra = 0

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'purchase_date', 'total', 'status', 'items_count']
    list_filter = ['status', 'purchase_date']
    search_fields = ['client__name', 'client__email']
    list_editable = ['status']
    readonly_fields = ['purchase_date', 'total', 'items_count']
    inlines = [PurchaseItemInline]
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('client', 'purchase_date', 'total', 'status')
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
    )
    
    def client_name(self, obj):
        return obj.client.name
    client_name.short_description = "Cliente"
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Itens"

@admin.register(ProductAction)
class ProductActionAdmin(admin.ModelAdmin):
    list_display = ['action_timestamp', 'admin', 'product', 'action_type']
    list_filter = ['action_type', 'action_timestamp']
    search_fields = ['product__name', 'admin__name']
    readonly_fields = ['action_timestamp']
    
    def has_add_permission(self, request):
        return False  # Actions are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Actions should not be editable