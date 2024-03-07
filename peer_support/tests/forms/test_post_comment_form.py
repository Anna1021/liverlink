from django.test import TestCase
from peer_support.forms import PostForm,CommentForm
from peer_support.models import User
from peer_support.models import Post

class CommentFormTestCase(TestCase):
    """Unit tests of the post comment form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
    ]

    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'content':"Test post comment."
        }
        self.post = Post.objects.get(pk=1)
    
    def test_form_valid_with_data(self):
        form_data = {'content': 'This is a valid comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    """
    def test_valid_comment_form(self):
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = CommentForm(self.comment)
        self.assertIn('content', form.fields)
    
    def test_form_has_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
    
    """

    def test_form_invalid_with_empty_body(self):
        form_data = {'content': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])