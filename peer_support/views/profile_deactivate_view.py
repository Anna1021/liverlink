from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

@login_required
def deactivate_user(request):
    """Deactivate the current user's account."""

    if request.method == "POST":
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        return redirect('home')
    return HttpResponseForbidden()