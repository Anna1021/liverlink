from django.contrib import admin
from .models import User, UserProfile, Patient, Parent

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
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'ethnicity', 'language', 'bio'
    ]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for patients."""

    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'ethnicity', 'language', 'bio', 'condition', 'age_of_diagnosis'
    ] 

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     """Configuration of the admin interface for parents."""

#     list_display = [
#         'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'ethnicity', 'language', 'bio', 'childs_condition', 'childs_age_of_diagnosis'
#     ]