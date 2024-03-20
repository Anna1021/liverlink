from django.contrib import admin
from .models import User, Patient, Parent, Mentor, Referral, UserProfile, Notification, Report

class UserProfileInline(admin.StackedInline):
    """Configuration of the admin interface for user profiles."""
    """Adds the user profile interface to the user interface."""
    model = UserProfile
    can_delete = False

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    
    ordering = ('username',)
    list_filter = ["is_active"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', "is_active" ]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for patients."""

    ordering = ('username',)
    list_filter = ["is_active"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', "is_active" 
    ] 

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for parents."""

    ordering = ('username',)
    list_filter = ["is_active"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', "is_active" 
    ]

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for mentors."""

    ordering = ('username',)
    list_filter = ["is_active"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', "is_active" 
    ]

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for referrals."""

    list_display = [
        'referrer', 'code'
    ]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for notifications."""

    ordering = ('title',)
    list_filter = ["viewed", "created"]
    list_display = [
        'id', 'title', 'created', 'viewed', 'user'
    ]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    list_filter = ["reason", "reported_at"]
    list_display = [
        'reason','reported_at'
    ]

    