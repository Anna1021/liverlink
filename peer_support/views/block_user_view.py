from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from peer_support.models import User

class BlockUserView(LoginRequiredMixin, View):
    """Block the specified user."""

    def get(self, request, user_id):
        blocked_user = User.objects.get(id=user_id)
        request.user.blocked_users.add(blocked_user)
        return JsonResponse({'status': 'success'})