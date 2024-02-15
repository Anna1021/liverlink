from django.test import TestCase
from peer_support.forms import NewResponseForm

class NewResponseFormTest(TestCase):
    """Unit tests of the Response form."""
    def test_form_valid_with_data(self):
        form_data = {'body': 'This is a valid response.'}
        form = NewResponseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_empty_body(self):
        form_data = {'body': ''}
        form = NewResponseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)
        self.assertEqual(form.errors['body'], ['This field is required.'])