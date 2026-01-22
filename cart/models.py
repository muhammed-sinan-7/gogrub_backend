from django.db import models
import uuid
from products.models import Product
from users.models import CustomUser
# Create your models here.
class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        return str(self.cart_id)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    
    def get_subtotal(self):
        return self.quantity * self.price
    
    
    class Meta:
        unique_together =("cart","product")
    def __str__(self):
        return str(self.cart)
    
    
