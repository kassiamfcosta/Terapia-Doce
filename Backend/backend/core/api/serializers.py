from rest_framework import serializers
from core.models import Product, Purchase, PurchaseItem, ProductAction
import json

class ProductSerializer(serializers.ModelSerializer):
    sizes = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'category', 
            'image', 'sizes', 'prices', 'is_active', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_sizes(self, obj):
        """Convert JSON string to list"""
        return obj.get_sizes()

    def get_prices(self, obj):
        """Convert JSON string to list"""
        return obj.get_prices()

    def create(self, validated_data):
        # Handle sizes and prices if they are provided as lists
        if 'sizes' in self.initial_data:
            sizes_list = self.initial_data['sizes']
            product = Product.objects.create(**validated_data)
            product.set_sizes(sizes_list)
            product.save()
        else:
            product = Product.objects.create(**validated_data)
        
        if 'prices' in self.initial_data:
            prices_list = self.initial_data['prices']
            product.set_prices(prices_list)
            product.save()
            
        return product

    def update(self, instance, validated_data):
        # Handle sizes and prices updates
        if 'sizes' in self.initial_data:
            instance.set_sizes(self.initial_data['sizes'])
        
        if 'prices' in self.initial_data:
            instance.set_prices(self.initial_data['prices'])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = PurchaseItem
        fields = [
            'id', 'product', 'product_name', 'quantity', 'price', 
            'size_selected', 'size_index'
        ]
        read_only_fields = ['id']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id', 'client', 'client_name', 'purchase_date', 'total', 
            'status', 'notes', 'items'
        ]
        read_only_fields = ['id', 'purchase_date']

class CreatePurchaseSerializer(serializers.ModelSerializer):
    items = serializers.ListField(write_only=True)
    
    class Meta:
        model = Purchase
        fields = ['total', 'notes', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        client = self.context['request'].user.client
        
        # Create purchase
        purchase = Purchase.objects.create(
            client=client,
            **validated_data
        )
        
        # Create purchase items
        for item_data in items_data:
            PurchaseItem.objects.create(
                purchase=purchase,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=item_data['price'],
                size_selected=item_data.get('size_selected', ''),
                size_index=item_data.get('size_index', 0)
            )
        
        return purchase

class ProductActionSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductAction
        fields = [
            'id', 'admin', 'admin_name', 'product', 'product_name',
            'action_type', 'action_timestamp', 'notes'
        ]
        read_only_fields = ['id', 'action_timestamp']