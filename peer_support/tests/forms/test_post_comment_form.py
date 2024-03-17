from django.test import TestCase
from peer_support.forms import PostForm,CommentForm
from peer_support.models import User,Post,PostComment

class CommentFormTestCase(TestCase):
    """Unit tests of the post comment form."""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_post_comment.json',
    ]

    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'content':"Test post comment."
        }
        self.post = Post.objects.get(pk=1)
    
    def test_form_valid_with_data(self):
        form = CommentForm(self.user,self.post,data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_empty_body(self):
        self.form_input['content'] = ''
        form = CommentForm(self.user,self.post,data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])

    def test_form_uses_model_validation(self):
        self.form_input['content'] = 'a'*256
        form = CommentForm(self.user,self.post,data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly_for_no_parent(self):
        form = CommentForm(self.user,self.post,data=self.form_input)
        before_count = PostComment.objects.count()
        direct_comments_before = self.post.get_comments().count()
        comment = form.save()
        after_count = PostComment.objects.count()
        direct_comments_after = self.post.get_comments().count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(direct_comments_after, direct_comments_before+1)
        self.assertEqual(comment.author,self.user)
        self.assertEqual(comment.content,"Test post comment.")
        self.assertEqual(comment.post,self.post)
        self.assertIsNone(comment.parent)

    def test_form_must_save_correctly_with_parent(self):
        parent_comment = PostComment.objects.get(pk=1)
        form = CommentForm(self.user,self.post,data=self.form_input)
        before_count = PostComment.objects.count()
        direct_comments_before = self.post.get_comments().count()
        comment = form.save(parent_id=parent_comment.pk)
        after_count = PostComment.objects.count()
        direct_comments_after = self.post.get_comments().count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(direct_comments_after, direct_comments_before)
        self.assertEqual(comment.author,self.user)
        self.assertEqual(comment.content,"Test post comment.")
        self.assertEqual(comment.post,self.post)
        self.assertEqual(comment.parent,parent_comment)