import json
from channels.generic.websocket import AsyncWebsocketConsumer
from peer_support.models import Message
from asgiref.sync import sync_to_async
 
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
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "message" : message , 
                "sender" : sender,
            })
    async def sendMessage(self , event) : 
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data = json.dumps({"message":message,"sender":sender}))