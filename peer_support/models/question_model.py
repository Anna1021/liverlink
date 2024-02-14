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

    # return the response directly to the question, will not return the response of another response
    def get_responses(self):
        return self.responses.filter(parent=None)