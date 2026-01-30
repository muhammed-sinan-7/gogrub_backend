from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")

        if not getattr(user, "is_authenticated", False):
            # close unauthenticated connections safely
            await self.close(code=4001)
            return

        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # ✅ CRITICAL SAFETY CHECK
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send_json({
            "id": event.get("id"),
            "title": event.get("title"),
            "message": event.get("message"),
            "created_at": event.get("created_at"),
        })
