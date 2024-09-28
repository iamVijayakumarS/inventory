# serializers.py
from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_Items
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        if Inventory_Items.objects.filter(name=value).exists():
            raise serializers.ValidationError("Item already exists.")
        return value
