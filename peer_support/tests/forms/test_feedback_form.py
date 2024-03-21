from django import forms
from django.test import TestCase
from peer_support.models import Feedback
from peer_support.forms import FeedbackForm

class FeedbackFormTestCase(TestCase):
    """Unit test of feedback form."""

    def setUp(self):
        self.form_input = {'title': 'Test', 'content': 'Test feedback'} 

    def test_form_validation(self):
        form = FeedbackForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = FeedbackForm(data=self.form_input)
        self.assertIn('title', form.fields)
        self.assertIn('content', form.fields)
        content_field = form.fields['content']
        self.assertTrue(isinstance(content_field.widget, forms.Textarea))

    def test_form_successfully_creates_feedback_object(self):
        before_count = Feedback.objects.count()
        form = FeedbackForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        form.save()
        after_count = Feedback.objects.count()
        self.assertEqual(before_count + 1, after_count)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.title, 'Test')
        self.assertEqual(feedback.content, 'Test feedback')

    def test_title_must_be_valid(self):
        self.form_input['title'] = 'x' * 51
        form = FeedbackForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_content_must_be_valid(self):
        self.form_input['content'] = 'x' * 501
        form = FeedbackForm(data=self.form_input)
        self.assertFalse(form.is_valid())