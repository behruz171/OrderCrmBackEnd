from django.db import models
from accounts.models import CustomUser
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('reviewing', 'Ko\'rib chiqilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    client_name = models.CharField(max_length=200, blank=True)
    client_phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Zayavka #{self.pk} - {self.client_name}"

    @property
    def total_sum(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def vat_sum(self):
        return round(self.total_sum * 12 / 100)

    @property
    def grand_total(self):
        return self.total_sum + self.vat_sum


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    # Snapshot fields — user can override these per-order
    name = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def vat_amount(self):
        return round(self.total_price * 12 / 100)

    @property
    def grand_total(self):
        return self.total_price + self.vat_amount
