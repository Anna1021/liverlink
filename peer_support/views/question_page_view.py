from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Question, Response, Notification
from peer_support.forms import NewReplyForm, NewResponseForm, ReportForm
from django.contrib import messages

class QuestionPageView(LoginRequiredMixin, View):
    """Displays a single question and all responses"""
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    max_depth = 20

    def get(self, request, id, *args, **kwargs):
        context = self.get_context(request, id)
        return render(request, 'question.html', context)
    
    def get_context(self, request ,question_id):
        question = get_object_or_404(Question, id=question_id)
        context = {
            'question': question,
            'response_form': NewResponseForm(),
            'reply_form': NewReplyForm(),
            'current_user': request.user,
            'report_form': ReportForm(),
            'max_depth': self.max_depth,
        }
        return context

    def post(self, request, id):
        if 'report_question' in request.POST:
            question_id = request.POST.get('action')
            self.question_report(request, question_id)
        elif 'report_response' in request.POST:
            response_id = request.POST.get('action')
            self.response_report(request, response_id)
        elif 'reply' in request.POST:
            self.reply_post(request)
        else:
            return self.response_post(request, id)
        return redirect('question', id=id)
    
    def response_post(self,request,id):
        response_form = NewResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user = request.user
            response.question = get_object_or_404(Question, id=id)
            response.save()
            self.send_notification_question(response)
            return redirect(f'/question/{id}#{response.id}')
        context = self.get_context(request, id)
        context['response_form']= response_form
        return render(request, 'question.html', context)
    
    def question_report(self, request, comment_id):
        question = get_object_or_404(Question, id=comment_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(question, request.user)
            messages.success(request, "Comment reported successfully.")
        else:
            messages.error(request, "There was an issue with the report.")

    def response_report(self, request, response_id):
        response = get_object_or_404(Response, id=response_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(response, request.user)
            messages.success(request, "Response reported successfully.")
        else:
            messages.error(request, "There was an issue with the response.")

    def reply_post(self, request):
        form = NewReplyForm(request.POST)
        if form.is_valid():
            question_id = request.POST.get('question')
            parent_id = request.POST.get('parent')
            reply = form.save(commit=False)
            reply.user = request.user
            reply.question = Question.objects.get(id=question_id)
            if parent_id:
                 reply.parent = Response.objects.get(id=parent_id)
            reply.save()
            self.send_notification_reply(reply)
            self.send_notification_question(reply)
        
    def send_notification_reply(self, reply):
        if reply.parent and reply.parent.user != reply.user:
            Notification.objects.create(content_object=reply, user=reply.parent.user, notifying_user=reply.user,
                                        description=f"{reply.user} has replied to your reply.")
        
    def send_notification_question(self, response):
        if response.user != response.question.author:
            Notification.objects.create(content_object=response, user=response.question.author, notifying_user=response.user)

