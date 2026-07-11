from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    vat_amount = serializers.ReadOnlyField()
    grand_total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'name', 'dimensions', 'description',
            'price', 'quantity', 'image_url',
            'total_price', 'vat_amount', 'grand_total',
        ]
        read_only_fields = ['id', 'total_price', 'vat_amount', 'grand_total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_sum = serializers.ReadOnlyField()
    vat_sum = serializers.ReadOnlyField()
    grand_total = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'client_name', 'client_phone', 'status', 'status_display',
            'notes', 'items', 'total_sum', 'vat_sum', 'grand_total',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_sum', 'vat_sum', 'grand_total', 'status_display']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance
