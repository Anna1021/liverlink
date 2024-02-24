from peer_support.models import Question
from django.shortcuts import render

def resources(request):
    """display the first 10 questions from newest to oldest"""
    questions = Question.objects.order_by('-created_at')
    context = {'questions': questions}
    return render(request, 'resources.html', context)