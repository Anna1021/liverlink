from django.contrib import admin
from .models import *


class UserProfileInline(admin.StackedInline):
    """Configuration of the admin interface for user profiles."""

    """Adds the user profile interface to the user interface."""
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    ordering = ("username",)
    search_fields = ("username", "id")
    list_filter = ["is_active", "date_joined"]
    inlines = [UserProfileInline]
    list_display = ["id", "username", "is_staff", "is_active"]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for patients."""

    ordering = ("username",)
    search_fields = ("username", "id")
    list_filter = ["is_active", "date_joined"]
    inlines = [UserProfileInline]
    list_display = ["id", "username", "is_active"]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for parents."""

    ordering = ("username",)
    search_fields = ("username", "id")
    list_filter = ["is_active", "date_joined"]
    inlines = [UserProfileInline]
    list_display = ["id", "username", "is_active"]


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for mentors."""

    ordering = ("username",)
    search_fields = ("username", "id")
    list_filter = ["is_active", "date_joined"]
    inlines = [UserProfileInline]
    list_display = ["id", "username", "is_active"]

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for professionals."""

    ordering = ("username",)
    search_fields = ("username", "id")
    list_filter = ["is_active", "date_joined"]
    inlines = [UserProfileInline]
    list_display = ["id", "username", "is_active", "referral_code"]

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for referrals."""

    list_display = ["referrer", "code"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for notifications."""

    ordering = ("title",)
    search_fields = ("title", "id", "user")
    list_filter = ["viewed", "created"]
    list_display = ["id", "title", "created", "viewed", "user"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    search_fields = ("reporter", "reason")
    list_filter = ["reason", "reported_at"]
    list_display = ["reporter", "reason", "reported_at"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    search_fields = ("author", "title")
    list_filter = ["created_at"]
    list_display = ["author", "title"]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for friend requests."""

    search_fields = ("user", "question")
    list_filter = ["created_at"]
    list_display = ["user", "question"]

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for feedback."""

    search_fields = ("title", "content")
    list_filter = ["submitted_at"]
    list_display = ["title"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for posts."""

    search_fields = ("author__username", "content")
    list_filter = ["created_at"]
    list_display = ["author"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(visibility='G') 