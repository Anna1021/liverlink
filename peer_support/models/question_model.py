from peer_support.models import User
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
    def get_responses(self):
        """return the response that is directly replying the question, will not return the reply of another response"""
        return self.responses.filter(parent=None)