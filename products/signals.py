# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import Product
# from notifications.services import notify_user
# from django.contrib.auth import get_user_model
# from users.models import CustomUser


# @receiver(pre_save, sender=Product)
# def product_price_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return

#     old_price = Product.objects.get(pk=instance.pk).price
#     if old_price != instance.price:
#         users = CustomUser.objects.all()
#         for user in users:
#             notify_user(
#                 user,
#                 "Price Updated",
#                 f"Price of {instance.name} has changed."
#             )
