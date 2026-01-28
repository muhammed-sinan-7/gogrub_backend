from rest_framework import serializers

from orders.models import Order, OrderItem
from products.models import Category, Product
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    category_name = serializers.StringRelatedField(source="category", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "category_name",
            "description",
            "image",
        ]


class ProductDetailSerialkizer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateUpdateSerialzier(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category", read_only=True)
    image = serializers.URLField()
    # price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "category",
            "category_name",
            "is_special",
            "is_available",
            "description",
            "image",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Invalid Amount: Price cannot be negative."
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category", read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "fullname", "is_active", "is_staff", "created_at"]


# class


class OrderItemListSerializer(serializers.ModelSerializer):
    # This reaches from OrderItem -> Order -> User -> fullname
    customer_name = serializers.ReadOnlyField(source="order.user.fullname")
    customer_email = serializers.ReadOnlyField(source="order.user.email")
    created_at = serializers.ReadOnlyField(source="order.created_at")
    payment_status = serializers.ReadOnlyField(source="order.payment_status")
    order_id = serializers.ReadOnlyField(source="order.id")
    order_status = serializers.ReadOnlyField(source="order.order_status")
    payment_method = serializers.ReadOnlyField(source="order.payment_method")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_id",
            "product_name",
            "quantity",
            "price",
            "subtotal",
            "customer_name",
            "customer_email",
            "order_id",
            "created_at",
            "payment_status",
            "order_status",
            "payment_method",
        ]


class AdminOrderSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="full_name")
    customer_email = serializers.EmailField(source="user.email")
    order_id = serializers.UUIDField(source="id")
    price = serializers.DecimalField(
        source="total_amount", max_digits=10, decimal_places=2
    )

    class Meta:
        model = Order
        fields = [
            "order_id",
            "customer_name",
            "customer_email",
            "price",
            "order_status",
            "payment_status",
            "payment_method",
            "created_at",
            "items",
        ]
