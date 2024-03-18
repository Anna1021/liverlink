from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from peer_support.models import Question

def delete_question(request, id):
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        messages.error(request, 'The question does not exist.')
        return redirect('resources') 

    if request.method == 'GET':
        question.delete()
        messages.success(request, 'The question has been deleted successfully.')
        return redirect('resources')
    else:
        context = {'question': question}
        return render(request, 'resources.html', context)

