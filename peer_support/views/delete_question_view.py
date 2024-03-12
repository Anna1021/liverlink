from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from peer_support.models import Question

def delete_question(request, id):
    question = get_object_or_404(Question, pk=id)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'The question has been deleted successfully.')
        return redirect('resources')
    else:
        context = {'question': question}
        return render(request, 'delete_question.html', context)
