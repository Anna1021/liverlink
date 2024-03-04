from peer_support.models import Question
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def resources(request):
    """display the first 10 questions from newest to oldest"""
    questions = Question.objects.order_by('-created_at')
    questions = questions.exclude(Q(author__in=request.user.blocked_users.all()) | Q(author__in=request.user.blocked_by.all()))
    context = {'questions': questions}
    return render(request, 'resources.html', context)