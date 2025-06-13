import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('stats', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('stats', self.channel_name)

    async def stats_update(self, event):
        await self.send(
            text_data=json.dumps(event['stats_box'])
        )
        


        

       