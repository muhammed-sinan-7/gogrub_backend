from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")

        if not user or isinstance(user, AnonymousUser):
            await self.close(code=4001)
            return

        self.user = user
        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

       
        await self.accept(subprotocol="jwt")

        print("✅ WS CONNECTED:", user.email)

    async def disconnect(self, close_code):
      
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

        print("⚠️ WS DISCONNECTED:", close_code)

    async def notify(self, event):
        await self.send_json(event["data"])
