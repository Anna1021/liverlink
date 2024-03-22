from django.utils import timezone
from django.db import models
from peer_support.models import User, Post


class PostComment(models.Model):
    """Model for Post Comments"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", null=True, default=None, blank=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def get_replies(self):
        """Return replies"""
        
        return PostComment.objects.filter(parent=self)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.content}'
