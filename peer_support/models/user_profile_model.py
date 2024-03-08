from django.db import models
from peer_support.models import User
from .model_choices import THEME_CHOICES, FONT_CHOICES, FONT_SIZE_CHOICES

class UserProfile(models.Model):
    """Model used for user profile settings (preferences)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length=500, blank=True, default='profile_pictures/Firefly Create a social media avatar of the night sky 96511.jpg')
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='DF')
    font = models.CharField(max_length=50, choices=FONT_CHOICES, default='DF')
    font_size = models.CharField(max_length=50, choices=FONT_SIZE_CHOICES, default='DF')