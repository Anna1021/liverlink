from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
from .model_choices import GENDER_CHOICES, ETHNICITY_CHOICES, LANGUAGE_CHOICES, COUNTRY_CHOICES, HOSPITAL_CHOICES


class User(AbstractUser):
    """Model used for user authentication and related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=50,choices=COUNTRY_CHOICES, blank=True)
    hospital = models.CharField(max_length=500, choices=HOSPITAL_CHOICES, blank=True)
    ethnicity = models.CharField(max_length=50,choices=ETHNICITY_CHOICES, blank=True)
    language = models.CharField(max_length=50,choices=LANGUAGE_CHOICES, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    conversations = models.ManyToManyField('Conversation',blank=True)

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)

    def sort_conversations(self):
        return self.conversations.order_by("-last_updated")
