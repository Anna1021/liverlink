from django.db import models
from django.utils import timezone
from peer_support.models import User

class Message(models.Model):
    """Model used for messages in a conversation"""
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=timezone.now)
    visible_to = models.ManyToManyField(User, blank=True,related_name='visible_to')
    read_by = models.ManyToManyField(User, blank=True,related_name = 'read_by')

    def delete(self,users):
        """Delete message"""
        self.visible_to.remove(users)
        print(self.visible_to.all())
        if self.visible_to.count() == 0:
            print('wow')
            Message.objects.filter(pk=self.pk).delete()

    def __str__(self):
        """Return a string representing the message"""
        return str(self.sender)+": "+self.content