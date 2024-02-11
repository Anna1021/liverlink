from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def deactivate_user(request):
    """Deactivate the current user's account."""

    user = request.user
    user.is_active = False
    user.save()
    messages.add_message(request, messages.SUCCESS, "Profile successfully deactivated!")
    logout(request)
    return redirect('home')