from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from peer_support.models import Question
from peer_support.forms import ReportForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from .helpers import get_page


class ResourcesView(LoginRequiredMixin, View):
    """Display questions and resources in chronological order."""
    
    def get(self, request):
        questions = Question.objects.order_by("-created_at")
        questions = get_page(request,questions)
        context = {"questions": questions, "report_form": ReportForm()}        
        return render(request, "resources.html", context)

        
    def post(self, request):
        question_id = request.POST.get("action")
        self.question_report(request, question_id)
        return redirect("resources")
    
    def question_report(self, request, comment_id):
        question = get_object_or_404(Question, id=comment_id)
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report_form.save_report_for_object(question, request.user)
            messages.success(request, "Question reported successfully.")
        else:
            messages.error(request, "There was an issue with the report.")

