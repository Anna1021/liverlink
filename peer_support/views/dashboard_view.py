from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user 
    if current_user.first_login == True:
        print("in the if statement")
        current_user.first_login = False
        current_user.save()
        return render(request, 'dashboard.html', {'user': current_user, 'first': True})
    return render(request, 'dashboard.html', {'user': current_user})