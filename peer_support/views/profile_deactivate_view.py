from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def deactivate_user(request):
    """Deactivate the current user's account."""

    if request.method == "POST":
        user = request.user
        user.is_active = False
        user.save()
        messages.add_message(request, messages.SUCCESS, "Profile successfully deactivated!")
        logout(request)
        return redirect('home')

    return HttpResponseForbidden()