from peer_support.models import Question
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def resources(request):
    """Display questions and resources in chronological order."""

    questions = Question.objects.order_by('-created_at')
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page') 
    questions = paginator.get_page(page_number)
    context = {'questions': questions}
    return render(request, 'resources.html', context)