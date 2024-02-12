from django.contrib import admin
from .models import User, Patient, Parent, Conversation, Notification, FriendRequest

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio'
    ]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for patients."""

    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'condition', 'age_of_diagnosis'
    ] 

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for parents."""

    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'child_condition', 'child_age_of_diagnosis'
    ]

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for conversations."""

    filter_vertical = ('users','messages')
    list_display = [
        'id'
    ]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for notifications."""

    list_display = [
        'id', 'title', 'description', 'created', 'viewed', 'user'
    ]

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    list_display = [
        'id','sender', 'receiver', 'is_accepted'
    ]