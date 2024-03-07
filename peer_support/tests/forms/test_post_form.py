from django.test import TestCase
from peer_support.forms import PostForm
from peer_support.models import User
from peer_support.models import Post

class PostFormTestCase(TestCase):
    """Unit tests of the post form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'text':"Test post."
        }
        self.post = Post.objects.get(pk=1)
    
    def test_valid_post_form(self):
        form = PostForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = PostForm(self.post)
        self.assertIn('text', form.fields)
    
    # def test_form_has_no_data(self):
    #     form = PostForm(data={})
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(len(form.errors),1)
    
    """
    def test_text_field_max_length(self):
        form = PostForm()
        self.assertEqual(form.fields['text'].max_length, 255)

    def test_text_must_not_contain_more_than_255_characters(self):
        self.form_input['text'] = 'x' * 256
        form = PostForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
    """

    def test_new_text_form_empty_text(self):
        form_data = self.form_input.copy()
        form_data['text'] = ''
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
        self.assertEqual(form.errors['text'],
                         ['This field is required.'])


