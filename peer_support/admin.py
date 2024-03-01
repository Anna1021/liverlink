from django.contrib import admin
from . import models
from .models import User, Patient, Parent, Mentor, Referral, Conversation, UserProfile, Notification, FriendRequest,Question,Response

from .models import Report
# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Response)

class UserProfileInline(admin.StackedInline):
    """Configuration of the admin interface for user profiles."""
    """Adds the user profile interface to the user interface."""
    model = UserProfile
    can_delete = False

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    
    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio'
    ]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for patients."""

    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'condition', 'age_of_diagnosis'
    ] 

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for parents."""

    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'child_condition', 'child_age_of_diagnosis'
    ]

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for mentors."""

    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'condition', 'age_of_diagnosis', 'referral_code'
    ]

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for referrals."""

    list_display = [
        'referrer', 'code'
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

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    list_display = [
        'reason','reported_at', 'content_type', 'object_id', 'content_object'
    ]