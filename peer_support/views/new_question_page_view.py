from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from peer_support.forms import  NewQuestionForm 

@login_required
def newQuestionPage(request):
    form = NewQuestionForm()
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('resources')
    context = {'form': form}
    return render(request, 'new-question.html', context)