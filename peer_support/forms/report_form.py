from django import forms
from peer_support.models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
