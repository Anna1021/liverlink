from peer_support.models import Question, Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from peer_support.forms import NewReplyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from peer_support.models import Question, Response
from peer_support.forms import NewReplyForm

@login_required(login_url='log_in')
def reply_page(request): # break this down @anna
    """Reply to the question"""

    if request.method == 'POST':
        form = NewReplyForm(request.POST)
        if form.is_valid():
            question_id = request.POST.get('question')
            parent_id = request.POST.get('parent')
            reply = form.save(commit=False)
            reply.user = request.user
            reply.question = Question(id=question_id)
            if parent_id:
                reply.parent = Response(id=parent_id)
            reply.save()
            return redirect(f'/question/{question_id}#{reply.id}')
        else:
            return render(request, 'resources.html', {'form': form})
    else:
        form = NewReplyForm()
    return render(request, 'resources.html', {'form': form})