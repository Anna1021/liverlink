from django.contrib import admin
from .models import User, Patient, Parent, Conversation, UserProfile

# Register your models here.

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
<<<<<<<<< Temporary merge branch 1

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for conversations."""

    filter_vertical = ('users','messages')
    list_display = [
        'id'
    ]
=========
>>>>>>>>> Temporary merge branch 2
