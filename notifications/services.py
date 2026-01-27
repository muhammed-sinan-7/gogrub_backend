import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification

logger = logging.getLogger(__name__)


def notify_user(user, title, message):
    logger.info(
        "notify_user called for user=%s title=%s", getattr(user, "id", user), title
    )

    notification = Notification.objects.create(user=user, title=title, message=message)

    logger.info("created notification id=%s for user=%s", notification.id, user.id)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "id": str(notification.id),
            "title": notification.title,
            "message": notification.message,
            "created_at": notification.created_at.isoformat(),
        },
    )
