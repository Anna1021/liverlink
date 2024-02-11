from django.db import models
from peer_support.models import User

class UserProfile(models.Model):
    """Model used for user profile settings (preferences)."""

    THEME_CHOICES = [
    ('DF', 'Default theme'),
    ('LM', 'Light mode'),
    ('DM', 'Dark mode'),
    ]

    FONT_CHOICES = [
    ('DF', 'Default font'),
    ('AR', 'Arial'),
    ('CA', 'Calibri'),
    ]

    FONT_SIZE_CHOICES = [
    ('DF', 'Default size'),
    ('LG', 'Large'),
    ('XL', 'Extra large'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='DF')
    font = models.CharField(max_length=50, choices=FONT_CHOICES, default='DF')
    font_size = models.CharField(max_length=50, choices=FONT_SIZE_CHOICES, default='DF')