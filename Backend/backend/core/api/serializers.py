from rest_framework import serializers
from core.models import Product, Purchase, PurchaseItem, ProductAction

# Serializer para Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'created_by']
        read_only_fields = ['id', 'created_by']

# Serializer para ProductAction
class ProductActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAction
        fields = ['id', 'admin', 'product', 'action_type', 'action_timestamp']
        read_only_fields = ['id', 'action_timestamp']

# Serializer para PurchaseItem
class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['id']

# Serializer para Purchase (com itens aninhados)
class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)  # campo aninhado

    class Meta:
        model = Purchase
        fields = ['id', 'client', 'purchase_date', 'total', 'status', 'items']
        read_only_fields = ['id', 'purchase_date']

    def validate(self, data):
        # Opcional: verifique se total bate com a soma dos items
        soma = sum(item['quantity'] * item['price'] for item in data['items'])
        if soma != data['total']:
            raise serializers.ValidationError(
                f"Total da compra ({data['total']}) não confere com a soma dos items ({soma})."
            )
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        for item in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item)
        return purchase
