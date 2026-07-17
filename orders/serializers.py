import base64
import os
import uuid
from django.conf import settings
from rest_framework import serializers
from .models import Order, OrderItem


def _save_base64_image(data_url):
    if not data_url or not data_url.startswith('data:image'):
        return data_url

    try:
        format, imgstr = data_url.split(';base64,')
        ext = format.split('/')[-1] or 'jpg'
        data = base64.b64decode(imgstr)

        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'order_items')
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(data)

        return f"{settings.MEDIA_URL}order_items/{filename}"
    except Exception:
        return ''


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    vat_amount = serializers.ReadOnlyField()
    grand_total = serializers.ReadOnlyField()
    image_url = serializers.CharField(required=False, allow_blank=True)

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

    def _resolve_image(self, url):
        if not url or not url.startswith('data:image'):
            return url
        path = _save_base64_image(url)
        request = self.context.get('request')
        if path.startswith('/') and request:
            return request.build_absolute_uri(path)
        return path

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            item_data['image_url'] = self._resolve_image(item_data.get('image_url', ''))
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
                item_data['image_url'] = self._resolve_image(item_data.get('image_url', ''))
                OrderItem.objects.create(order=instance, **item_data)
        return instance
