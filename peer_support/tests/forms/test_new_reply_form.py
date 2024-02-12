from django.test import TestCase
from peer_support.forms import NewReplyForm

class NewReplyFormTest(TestCase):

    def test_form_valid_with_data(self):
        form_data = {'body': 'This is a valid response.'}
        form = NewReplyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_empty_body(self):
        form_data = {'body': ''}
        form = NewReplyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)
        self.assertEqual(form.errors['body'], ['This field is required.'])

    def test_placeholder_in_body_widget(self):
        form = NewReplyForm()
        self.assertEqual(form.fields['body'].widget.attrs['placeholder'], 'What are your thoughts?')

    def test_rows_attribute_in_body_widget(self):
        form = NewReplyForm()
        self.assertEqual(form.fields['body'].widget.attrs['rows'], 5)
