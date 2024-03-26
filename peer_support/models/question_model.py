from peer_support.models import User
from django.db import models


class Question(models.Model):
    """Model used for questions in the peer support forum"""

    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_responses(self):
        """Return direct responses to the question"""

        return self.responses.filter(parent=None)
