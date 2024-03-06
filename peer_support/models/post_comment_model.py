from django.utils import timezone
from django.db import models
from peer_support.models import User, Post


class PostComment(models.Model):
    """Model for Post Comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.text}'
    
    def get_delete_str(self):
        return self.__str__()