from rest_framework import serializers
from .models import Cart,CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    product_image = serializers.CharField(source='product.image',read_only=True)
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields =['id','product','product_name','product_image','quantity','price','subtotal']
        
    def get_subtotal(self,obj):
        return obj.get_subtotal()
    
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer()
    total = serializers.DecimalField(max_digits=10,decimal_places=2,source='get_total')
    item_count = serializers.IntegerField(source='get_item_count', read_only=True)
    class Meta:
         model = Cart
         fields =['cart_id','items','total','item_count']
         