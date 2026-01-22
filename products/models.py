from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_special = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    image = models.URLField()
    
    def __str__(self):
        return self.name
    
    