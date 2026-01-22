from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from products.models import Product,Category
from cart.models import Cart,CartItem
from wishlist.models import Wishlist,WishlistItem
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'fullname', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_active', 'created_at']
    search_fields = ['email', 'fullname']
    ordering = ['-created_at']
    
    # Fields to display when viewing/editing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('fullname', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    # Fields to display when creating new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'user', 'get_item_count', 'get_total', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['cart_id', 'user__email']
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total'
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'price', 'get_subtotal']
    list_filter = ['cart', 'product']
    search_fields = ['cart__cart_id', 'product__name']
    
    
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(WishlistItem)
admin.site.register(Wishlist)

