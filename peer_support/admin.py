from django.contrib import admin
from .models import User, Patient, Parent, Conversation, Mentor, Referral

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

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for mentors."""

    list_display = [
        'id','username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'location', 'ethnicity', 'language', 'bio', 'mentor_condition', 'mentor_age_of_diagnosis'
    ]

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for referrals."""

    list_display = [
        'referrer','referred','code','claimed'
    ]