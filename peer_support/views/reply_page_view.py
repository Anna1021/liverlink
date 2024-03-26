from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Question, Response, Notification
from peer_support.forms import NewReplyForm


class ReplyPageView(LoginRequiredMixin, View):
    """Allows users to reply to a question"""

    template_name = 'resources.html'
    form_class = NewReplyForm
    max_depth = 10

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'MAX_DEPTH': self.max_depth})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            question_id = request.POST.get('question')
            parent_id = request.POST.get('parent')
            if parent_id:
                parent_response = Response.objects.get(id=parent_id)
                if parent_response.get_depth() >= self.max_depth:
                    return render(request, 'question.html', {'form': form, 'MAX_DEPTH': self.max_depth , 'error': 'Maximum reply depth exceeded.'})
                
            reply = form.save(commit=False)
            reply.user = request.user
            reply.question = Question.objects.get(id=question_id)
            if parent_id:
                 reply.parent = Response.objects.get(id=parent_id)
            reply.save()
            self.send_notification(reply)
            return render(request, 'question.html', {'form': form, 'MAX_DEPTH': self.max_depth})
        else:
            return render(request, 'resources.html', {'form': form})
        
    def send_notification(self, reply):
        """Send a notification to the question author and parent author."""
        
        if reply.parent and reply.parent.user != reply.user:
            Notification.objects.create(content_object=reply, user=reply.parent.user, notifying_user=reply.user,
                                        description=f"{reply.user} has replied to your reply.")
        if reply.user != reply.question.author:
            Notification.objects.create(content_object=reply, user=reply.question.author, notifying_user=reply.user)

