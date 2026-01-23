from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user(user, title, message):
    # 1. Store
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )

    # 2. Send real-time
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "title": title,
            "message": message,
        }
    )