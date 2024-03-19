from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from peer_support.models import Question
def delete_question(request, id):
    """Delete a question."""

    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        messages.error(request, 'The question does not exist.')
        return redirect('resources') 
    question.delete()
    messages.success(request, 'The question has been deleted successfully.')
    return redirect('resources')