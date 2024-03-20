from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from peer_support.models import User

class Notification(models.Model):
    """Model used for notifications."""
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifying_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'notifications_sent', null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def set_title(self):
        """Set the title of the notification based on its content_type."""

        self.title = "New " + self.content_type.name.title()

    def set_description(self):
        """Set the description of the notification based on its content_type."""

        descriptions = {'friend request' : f"{self.notifying_user.username} has sent you a friend request.",
                        'post comment' : f"{self.notifying_user.username} has commented on your post.",
                        'response' : f"{self.notifying_user.username} has replied to your question.",
                        'conversation' : f"{self.notifying_user.username} has created a conversation with you.",
                        'group conversation' : f"{self.notifying_user.username} has added you to a group conversation."}

        self.description = descriptions[self.content_type.name]

    def get_URL(self):
        """Return the URL to use (to access the content_object) for the notification page."""

        if self.content_object:
            if self.content_type.name == 'post comment':
                return self.get_post_URL()
            elif self.content_type.name == 'conversation' or self.content_type.name == 'group conversation':
                return self.get_conversation_URL()
            elif self.content_type.name == 'response':
                return self.get_question_URL()

        return reverse('profile', kwargs={'username': self.notifying_user})
    
    def get_post_URL(self):
        """Return the URL to the post being replied to, if the post still exists."""

        return reverse('post_detail', kwargs={'post_id': self.content_object.post.id})
    
    def get_question_URL(self):
        """Return the URL to the question being replied to."""

        return reverse('question', kwargs={'id': self.content_object.question.id})
    
    def get_conversation_URL(self):
        """Return the URL of the conversation the user has been added to."""

        return reverse('conversation', kwargs={'conversation_id': self.content_object.id})
    
    def get_is_friend_request(self):
        """Return whether the notification is for a friend request."""

        if self.content_type:
            return self.content_type.name == 'friend request'
        return False

    def save(self, *args, **kwargs):
        """Save the notification with the correct title and description."""

        if self.content_type:
            if self.content_type.name == 'conversation' and not self.notifying_user:
                self.notifying_user = self.content_object.users.exclude(username=self.user.username)
            if not self.title:
                self.set_title()
            if not self.description:
                self.set_description()
        super().save(*args, **kwargs)