import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Unirse a un grupo llamado "dashboard"
        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard("dashboard", self.channel_name)

    # Recibir un mensaje del grupo "dashboard"
    async def dashboard_update(self, event):
        new_data = event['data']
        # Enviar datos al cliente WebSocket
        await self.send(text_data=json.dumps(new_data))
