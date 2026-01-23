from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from notifications.services import notify_user
from django.contrib.auth import get_user_model
from users.models import CustomUser




@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if not created:
        return

    notify_user(
        instance.user,
        "Order Placed",
        f"Your order #{instance.id} has been placed."
    )

    admins = CustomUser.objects.filter(is_staff=True)
    for admin in admins:
        notify_user(
            admin,
            "New Order Arrived",
            f"Order #{instance.id} placed by {instance.user.email}"
        )


@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, created, **kwargs):
    if created:
        return

    notify_user(
        instance.user,
        "Order Updated",
        f"Your order #{instance.id} is now {instance.status}"
    )


from django.db.models.signals import pre_save
from django.dispatch import receiver
from products.models import Product
from notifications.services import notify_user
from django.contrib.auth import get_user_model
from users.models import CustomUser


@receiver(pre_save, sender=Product)
def product_price_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_price = Product.objects.get(pk=instance.pk).price
    if old_price != instance.price:
        users = CustomUser.objects.all()
        for user in users:
            notify_user(
                user,
                "Price Updated",
                f"Price of {instance.name} has changed."
            )
