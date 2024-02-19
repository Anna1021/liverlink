from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from peer_support.models import User

@login_required
def friends_list(request):
    user = request.user
    friends = user.friends.all()
    context = {'friends': friends}
    return render(request, 'friends_list.html', context)