from django.db import models
from django.utils import timezone
from peer_support.models import User

class Message(models.Model):
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.sender)+": "+self.content