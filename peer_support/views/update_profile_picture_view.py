import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from peer_support.models import UserProfile


@login_required
@require_POST
def update_profile_picture(request):
    """Updates user's profile picture"""

    data = json.loads(request.body)
    profile_picture = data.get("profile_picture")
    if not profile_picture:
        return JsonResponse({"status": "fail"})
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.profile_picture = profile_picture
    user_profile.save()
    messages.add_message(request, messages.SUCCESS, "Profile picture updated!")
    return JsonResponse({"status": "success"})
