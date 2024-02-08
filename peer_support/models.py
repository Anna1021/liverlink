from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
import pycountry
from django.core.validators import MinValueValidator
from django.utils import timezone

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

    # TODO:
    # - 
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

class Patient(User):
    """Model used for patient authentication, and patient related information."""

    condition = models.CharField(max_length=50, blank=True, null=True)
    age_of_diagnosis = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Parent(User):
    """Model used for parent authentication, and parent related information."""
    
    # child = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    child_condition = models.CharField(max_length=50, blank=True, null=True)
    child_age_of_diagnosis = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'

class Mentor(User):
    """Model used for mentor authentication, and mentor related information."""
    
    mentor_condition = models.CharField(max_length=50, blank=True, null=True)
    mentor_age_of_diagnosis = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    # qualifications ??

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

class Message(models.Model):
    sender = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,unique=False)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(default=timezone.now)

class Conversation(models.Model):
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)

    def add_user(self,user):
        """Adds user to a group"""
        self.users.add(user)

    def send(self,message):
        """Sends message to the conversation"""
        self.messages.add(message)
        for user in self.users.exclude(username=message.sender.username):
            user.update_unread_messages(message)

    def as_group(self):
        """Return object as an instance of GroupConversation"""
        try:
            return self.groupconversation
        except GroupConversation.DoesNotExist:
            return None

    def get_first_member(self):
        return self.users.all([0])

    def get_second_member(self):
        return self.users.all([1])    

class GroupConversation(Conversation):
    name = models.CharField(max_length=20,null=True)

    def remove_user(self,user):
        if self.group:
            self.users.remove(user)
            if self.users.count()==0:
                Message.objects.filter(pk=self.pk).delete() #completely deletes conversation if no member left

    def display_name(self):
        if self.name is None:
            members = self.users.all()
            return ", ".join([i.username for i in members]) #automatically ordered by username
        return self.name

    