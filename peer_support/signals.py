"""Signal dispatcher for peer_support."""
from django.db.models.signals import post_save
from .models import User, UserProfile

def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a User is created."""
    
    # Do not run signal during test fixtures
    if created and not UserProfile.objects.filter(user=instance).exists() and not kwargs.get('raw', False):
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
for subclass in User.__subclasses__():
    post_save.connect(create_user_profile, sender=subclass)