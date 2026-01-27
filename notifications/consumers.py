from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")
        # Use is_authenticated test instead of comparing to AnonymousUser()
        if not getattr(user, "is_authenticated", False):
            await self.close()
            return

        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Renamed to match the event type "send_notification" sent from server
    async def send_notification(self, event):
        await self.send_json(
            {
                "id": event.get("id"),
                "title": event.get("title"),
                "message": event.get("message"),
                "created_at": event.get("created_at"),
            }
        )
