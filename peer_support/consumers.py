import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time
from channels.db import database_sync_to_async
 
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
            self.channel_name 
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender = text_data_json["sender"]
        conversation_id = text_data_json["conversation_id"]
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "sender":sender,
                "conversation_id":conversation_id,
            })
    async def sendMessage(self , event) :
        time.sleep(0.1)
        sender = event["sender"]
        conversation_id = int(event["conversation_id"])
        usernames = await self.get_users(conversation_id)
        await self.send(text_data = json.dumps({"sender":sender,"users":str(usernames)[2:-2]}))

    @database_sync_to_async
    def get_users(self,conversation_id):
        from peer_support.models import Conversation
        conversation = Conversation.objects.get(id=conversation_id)
        users = list(conversation.users.all())
        return list(map(lambda user: user.username,users))