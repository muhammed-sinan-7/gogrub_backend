# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from notifications.services import notify_user
# from django.contrib.auth import get_user_model
# from users.models import CustomUser


# @receiver(post_save, sender=Order)
# def order_created(sender, instance, created, **kwargs):
#     if not created:
#         return

#     notify_user(
#         instance.user,
#         # "Order Placed",
#         f"Your order #{instance.id} has been placed."
#     )

#     admins = CustomUser.objects.filter(is_staff=True)
#     for admin in admins:
#         notify_user(
#             admin,
#             "New Order Arrived",
#             f"Order #{instance.id} placed by {instance.user.email}"
#         )


# @receiver(post_save, sender=Order)
# def order_status_updated(sender, instance, created, **kwargs):
#     if created:
#         return

#     notify_user(
#         instance.user,
#         "Order Updated",
#         f"Your order #{instance.id} is now {instance.status}"
#     )
