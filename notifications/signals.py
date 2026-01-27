import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

from orders.models import Order
from products.models import Product
from users.models import CustomUser

from .services import notify_user  # keep notify_user in a services module


# =========================
# ORDER CREATED
# =========================
@receiver(post_save, sender=Order, dispatch_uid="notifications.order_created")
def order_created(sender, instance, created, **kwargs):
    if not created:
        return

    logger.info(
        "order_created signal for Order %s user=%s", instance.pk, instance.user_id
    )

    # Notify order user
    notify_user(
        instance.user, "Order Placed", f"Your order #{instance.id} has been placed."
    )

    # Admin notifications (exclude the order user if they are staff)
    admins = CustomUser.objects.filter(is_staff=True).exclude(pk=instance.user_id)
    for admin in admins:
        notify_user(
            admin,
            "New Order Arrived",
            f"Order #{instance.id} placed by {instance.user.email}",
        )


@receiver(post_save, sender=Order, dispatch_uid="notifications.order_status_changed")
def order_status_changed(sender, instance, created, update_fields, **kwargs):
    if created or (update_fields and "order_status" not in update_fields):
        return

    old_status = getattr(instance, "_old_status", None)
    if old_status == instance.order_status:
        return

    notify_user(
        instance.user,
        "Order Updated",
        f"Your order #{instance.id} is now {instance.order_status}",
    )


@receiver(pre_save, sender=Product, dispatch_uid="notifications.product_price_change")
def product_price_change(sender, instance, **kwargs):
    """
    Notify users when product price changes
    """
    if not instance.pk:
        return

    try:
        old_price = Product.objects.values_list("price", flat=True).get(pk=instance.pk)
    except Product.DoesNotExist:
        return

    if old_price == instance.price:
        return

    users = CustomUser.objects.all()
    for user in users:
        notify_user(user, "Price Updated", f"Price of {instance.name} has changed.")


@receiver(pre_save, sender=Order, dispatch_uid="notifications.cache_old_status")
def cache_old_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_status = None
        return

    try:
        db_instance = Order.objects.only("order_status").get(pk=instance.pk)
        instance._old_status = db_instance.order_status
    except Order.DoesNotExist:
        instance._old_status = None
