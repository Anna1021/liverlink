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
    notifying_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'notifications_sent', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_title(self):
        """Get the title of the notification based on its content_type."""

        return "New " + self.content_type.name.title()

    def get_description(self):
        """Get the description of the notification based on its content_type."""

        if self.notifying_user:
            descriptions = {
                "friend request": f"{self.notifying_user.username} has sent you a friend request.",
                "post comment": f"{self.notifying_user.username} has commented on your post.",
                "post": f"{self.notifying_user.username} has liked your post.",
                "response": f"{self.notifying_user.username} has replied to your question.",
                "conversation": f"{self.notifying_user.username} has created a conversation with you.",
                "group conversation": f"{self.notifying_user.username} has added you to a group conversation.",
            }
            if self.content_type.name in descriptions.keys():
                return descriptions[self.content_type.name]
        return f"Content type '{self.content_type.name}' has no default description."

    def set_default_fields(self):
        """If the notification has no content_object, set the title and description fields to a default."""

        if not self.title:
            self.title = "Default Title"
        if not self.description:
            self.description = "Default description"

    def get_URL(self):
        """Return the URL to use (to access the content_object) for the notification page."""

        if self.content_object:
            if self.content_type.name == 'post comment' or self.content_type.name == 'post':
                return self.get_post_URL()
            elif self.content_type.name == 'conversation' or self.content_type.name == 'group conversation':
                return self.get_conversation_URL()
            elif self.content_type.name == 'response':
                return self.get_question_URL()
        if self.notifying_user:
            return reverse('profile', kwargs={'username': self.notifying_user})
        else:
            return reverse('inbox')

    def get_post_URL(self):
        """Return the URL to the post liked / being replied to, if the post still exists."""

        post_id = (
            self.content_object.id
            if self.content_type.name == "post"
            else self.content_object.post.id
        )
        return reverse("post", kwargs={"post_id": post_id})

    def get_question_URL(self):
        """Return the URL to the question being replied to."""

        return reverse("question", kwargs={"id": self.content_object.question.id})

    def get_conversation_URL(self):
        """Return the URL of the conversation the user has been added to."""

        return reverse("conversation", kwargs={"conversation_id": self.content_object.id})

    def get_is_friend_request(self):
        """Return whether the notification is for a friend request."""

        if self.content_type:
            return self.content_type.name == "friend request"
        return False

    def save(self, *args, **kwargs):
        """Save the notification with the correct title and description."""

        if self.content_type:
            if not self.title:
                self.title = self.get_title()
            if not self.description:
                self.description = self.get_description()
        else:
            self.set_default_fields()
        super().save(*args, **kwargs)
