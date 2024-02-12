from django.test import TestCase
from peer_support.forms import NewQuestionForm

class QuestionFormTest(TestCase):
    def setUp(self):
        self.form_input = {
            'title': 'Test Question',
            'body': 'This is a test question body.'
        }

    def test_valid_sign_up_form(self):
        form = NewQuestionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    def test_new_question_form_no_data(self):
        form = NewQuestionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_title_field_max_length(self):
        form = NewQuestionForm()
        self.assertEqual(form.fields['title'].max_length, 150)

    def test_new_question_form_empty_title(self):
        form_data = self.form_input.copy()
        form_data['title'] = ''
        form = NewQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'],
                         ['This field is required.'])

    def test_new_question_form_empty_body(self):
        form_data = self.form_input.copy()
        form_data['body'] = ''
        form = NewQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)
        self.assertEqual(form.errors['body'],
                         ['This field is required.'])