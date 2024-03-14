from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Question, Response
from peer_support.forms import NewReplyForm

class ReplyPageView(LoginRequiredMixin, View):
    """reply to the question"""
    
    template_name = 'resources.html'
    form_class = NewReplyForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            question_id = request.POST.get('question')
            parent_id = request.POST.get('parent')
            reply = form.save(commit=False)
            reply.user = request.user
            reply.question = Question.objects.get(id=question_id)
            if parent_id:
                reply.parent = Response.objects.get(id=parent_id)
            reply.save()
            return redirect(f'/question/{question_id}#{reply.id}')
        else:
            return render(request, self.template_name, {'form': form})
