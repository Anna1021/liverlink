from peer_support.models import Question
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def resources(request):
    """Display questions and resources in chronological order."""

    questions = Question.objects.order_by('-created_at')
    context = {'questions': questions}
    return render(request, 'resources.html', context)