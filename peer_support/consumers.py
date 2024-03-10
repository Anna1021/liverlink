import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time
 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_layer 
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json["sender"]
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "sender":sender,
            })
    async def sendMessage(self , event) :
        time.sleep(0.1)
        sender = event["sender"]
        await self.send(text_data = json.dumps({"sender":sender}))