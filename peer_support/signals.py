"""Signal dispatcher for peer_support."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, Patient, Parent

@receiver (post_save)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a User is created."""

    if issubclass(sender, User):
        if created:
            UserProfile.objects.create(user=instance)