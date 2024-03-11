from django import forms
from peer_support.models import Report
from django.contrib.contenttypes.models import ContentType
class ReportForm(forms.ModelForm):
    """Form enabling users to report content"""
    class Meta:
        model = Report
        fields = ['reason']

    def save_report_for_object(self, obj, user):
        """Saves report based on content type"""
        if not self.is_valid():
            raise ValueError("Cannot save report: the form is not valid.")
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.reporter = user
        self.instance.object_id = obj.pk
        return super().save(commit=True)