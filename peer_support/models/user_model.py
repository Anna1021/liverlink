from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
import pycountry

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]

    ETHNICITY_CHOICES = [
        ('Asian or Asian British', [
            ('IN', 'Indian'),
            ('PK', 'Pakistani'),
            ('BD', 'Bangladeshi'),
            ('CH', 'Chinese'),
            ('OA', 'Any other Asian background'),
        ]),
        ('Black, Black British, Caribbean or African', [
            ('CB', 'Caribbean'),
            ('AF', 'African'),
            ('OB', 'Any other Black, Black British, or Caribbean background'),
        ]),
        ('Mixed or multiple ethnic groups', [
            ('WC', 'White and Black Caribbean'),
            ('WA', 'White and Black African'),
            ('WS', 'White and Asian'),
            ('OM', 'Any other Mixed or multiple ethnic background'),
        ]),
        ('White', [
            ('BR', 'English, Welsh, Scottish, Northern Irish or British'),
            ('IR', 'Irish'),
            ('GT', 'Gypsy or Irish Traveller'),
            ('RO', 'Roma'),
            ('OW', 'Any other White background'),
        ]),
        ('Other ethnic group', [
            ('AR', 'Arab'),
            ('OG', 'Any other ethnic group'),
        ]),
    ]

    LANGUAGE_CHOICES = sorted(
        [(lang.alpha_2, lang.name) for lang in pycountry.languages if hasattr(lang, 'alpha_2')],
        key=lambda x: x[1]
    )

    COUNTRY_CHOICES = sorted(
        [(country.alpha_2, country.name) for country in pycountry.countries],
        key=lambda x: x[1]
    )

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
    ethnicity = models.CharField(max_length=50,choices=ETHNICITY_CHOICES, blank=True)
    language = models.CharField(max_length=50,choices=LANGUAGE_CHOICES, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    conversations = models.ManyToManyField('Conversation')
    unread_messages = models.ManyToManyField('Message')

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
      
    def update_unread_messages(self,message):
        self.unread_messages.add(message)
