from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import User, FriendRequest

class ProfileView(LoginRequiredMixin, View):
    """Displays other user's profile"""
    
    def get(self, request, username):
        """Get request for user to view profile"""
        user = User.objects.get(username=username)
        context = {'user': user, 'current_user': request.user}

        if hasattr(user, 'parent'):
            context['parent'] = user.parent
        elif hasattr(user, 'patient'):
            context['patient'] = user.patient
        else:
            context['mentor'] = user.mentor

        context['blocklist'] = request.user.blocked_users.all() | user.blocked_users.all()
        context['is_friend'] = request.user in user.friends.all()
        context['request_sent'] = FriendRequest.objects.filter(sender=request.user, receiver=user).exists()

        return render(request, 'profile.html', context)