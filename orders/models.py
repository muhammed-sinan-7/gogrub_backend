from django.db import models
import uuid
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )
    
    ORDER_CHOICES = (
        ("processing","Processing"),
        ("shipped","Shipped"),
        ("delivered","Delivered"),
        ("cancelled","Cancelled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    order_status = models.CharField(ORDER_CHOICES, default='processing',max_length=20)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    street = models.TextField()
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)

    # Replace Stripe fields with Razorpay fields
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.fullname}"

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    product_image = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
