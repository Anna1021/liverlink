from django.contrib.contenttypes.models import ContentType
from peer_support.models import User, Message, Post

def get_message(data):
    return Message.objects.filter(sender=get_user(data["sender"]).pk).first()

def get_user(data):
    return User.objects.get(username=data["username"])

def get_content_type(model_name):
    return ContentType.objects.get(model=model_name)

def get_post(data):
    return Post.objects.filter(content=data["content"]).first()