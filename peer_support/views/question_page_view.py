from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Question
from peer_support.forms import NewReplyForm, NewResponseForm
from .helpers import send_notification

class QuestionPageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id, *args, **kwargs):
        question = get_object_or_404(Question, id=id)
        response_form = NewResponseForm()
        reply_form = NewReplyForm()
        context = {
            'question': question,
            'response_form': response_form,
            'reply_form': reply_form,
            'current_user': request.user,
        }
        return render(request, 'question.html', context)

    def post(self, request, id):
        response_form = NewResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user = request.user
            response.question = get_object_or_404(Question, id=id)
            response.save()
            send_notification(response)
            return redirect(f'/question/{id}#{response.id}')
        question = get_object_or_404(Question, id=id)
        reply_form = NewReplyForm() 
        context = {
            'question': question,
            'response_form': response_form,
            'reply_form': reply_form,
            'current_user': request.user,
        }
        return render(request, 'question.html', context)