from django.contrib import admin
from .models import User, Patient, Parent, Mentor, Referral, Conversation, UserProfile, Notification, FriendRequest, Report, Message, Post

class UserProfileInline(admin.StackedInline):
    """Configuration of the admin interface for user profiles."""
    """Adds the user profile interface to the user interface."""
    model = UserProfile
    can_delete = False

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    
    list_filter = ["date_of_birth", "gender", "location", "hospital", "ethnicity", "language"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio'
    ]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for patients."""

    list_filter = ["date_of_birth", "gender", "location", "hospital", "ethnicity", "language", "condition", "transplant", "age_of_diagnosis"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'condition', 'age_of_diagnosis', 'transplant'
    ] 

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for parents."""

    list_filter = ["date_of_birth", "gender", "location", "hospital", "ethnicity", "language", "child_condition", "child_transplant", "child_age_of_diagnosis"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'child_condition', 'child_age_of_diagnosis', 'child_transplant'
    ]

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for mentors."""

    list_filter = ["date_of_birth", "gender", "location", "hospital", "ethnicity", "language", "condition", "transplant", "age_of_diagnosis"]
    inlines = [UserProfileInline]
    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'hospital', 'ethnicity', 'language', 'bio', 'condition', 'age_of_diagnosis', 'referral_code', 'transplant'
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

    list_filter = ["viewed", "created"]
    list_display = [
        'id', 'title', 'description', 'created', 'viewed', 'user'
    ]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    list_filter = ["reason", "reported_at"]
    list_display = [
        'reason','reported_at', 'content_type', 'object_id', 'content_object'
    ]

    