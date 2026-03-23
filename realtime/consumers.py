from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MainConsumer(AsyncWebsocketConsumer):
    """ class MainConsumer
    """

    async def connect(self) -> None:
        """ connect
        """
        self.group_name = "main"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.update_online_count(1)

    async def disconnect(self, close_code) -> None:
        """ disconnect
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.update_online_count(-1)

    async def receive(self, text_data) -> None:
        """ receive
        """
        data = json.loads(text_data)
        user = self.scope["user"]
        msg_type = data.get("type")

        if msg_type == "chat":
            if user.is_authenticated:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "broadcast_chat",
                        "message": data["message"],
                        "username": user.username
                    }
                )
            else:
                await self.send(json.dumps({
                    "type": "error",
                    "message": "Login required"
                }))

        elif msg_type == "notification":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "broadcast_notification",
                    "message": data["message"]
                }
            )

    async def update_online_count(self, delta) -> None:
        """ delta = +1 при підключенні, -1 при відключенні
        """

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_online_delta",
                "delta": delta
            }
        )

    async def broadcast_online_delta(self, event) -> None:
        """ Handles incremental updates of online users
        """

        if not hasattr(self.channel_layer, "_online_count"):
            self.channel_layer._online_count = 0
        self.channel_layer._online_count += event["delta"]
        count = self.channel_layer._online_count

        await self.send(json.dumps({
            "type": "online",
            "count": count
        }))

    async def broadcast_chat(self, event) -> None:
        """Handles chat messages
        """

        await self.send(json.dumps({
            "type": "chat",
            "message": event["message"],
            "username": event["username"]
        }))

    async def broadcast_notification(self, event) -> None:
        """Handles notifications
        """
        await self.send(json.dumps({
            "type": "notification",
            "message": event["message"]
        }))
