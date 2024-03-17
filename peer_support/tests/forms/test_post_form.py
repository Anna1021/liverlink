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
            'text':"Test post.",
            'visibility':"G"
        }
        self.post = Post.objects.get(pk=1)
    
    def test_valid_post_form(self):
        form = PostForm(self.user,data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = PostForm(self.user)
        self.assertIn('text', form.fields)
        self.assertIn('visibility',form.fields)
    
    def test_form_uses_model_validation(self):
        self.form_input['text'] = 'x' * 281
        form = PostForm(self.user,data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_new_text_form_empty_text(self):
        form_data = self.form_input.copy()
        form_data['text'] = ''
        form = PostForm(self.user,data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
        self.assertEqual(form.errors['text'],
                         ['This field is required.'])

    def test_form_must_save_correctly(self):
        form = PostForm(self.user,data=self.form_input)
        before_count = Post.objects.count()
        post = form.save()
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(post.author,self.user)
        self.assertEqual(post.text,"Test post.")
        self.assertEqual(post.visibility,"G")

