# clients/api/serializers.py
from rest_framework import serializers  # <- Esta linha estava faltando
from clients.models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'address']
        read_only_fields = ['id']