from rest_framework import serializers
from admins.models import Admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'name', 'email', 'role']
        read_only_fields = ['id']
