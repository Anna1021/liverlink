from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from peer_support.utils import create_referral

@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user 
    return render(request, 'dashboard.html', {'user': current_user})