from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Post, PostComment, User

class PostCommentModelTestCase(TestCase):
    """Unit tests for the Post Comment model."""
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_post.json',
        'peer_support/tests/fixtures/default_post_comment.json',
        'peer_support/tests/fixtures/other_comments.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.post = Post.objects.get(pk=1)
        self.comment = PostComment.objects.get(pk=1)
    
    # Create a comment
        
    def test_valid_comment(self):
        self._assert_comment_is_valid()

    def test_correct_author(self):
        self.assertEqual(self.comment.author,self.user)

    def test_correct_content(self):
        self.assertEqual(self.comment.content,"This is a default comment.")

    def test_timestamp_is_not_null(self):
        self.assertIsNotNone(self.comment.created_at)
    
    def test_comment_content_must_have_at_least_one_character(self):
        self.comment.content = ""
        self._assert_comment_is_invalid()

    def test_comment_content_must_not_contain_more_than_255_characters(self):
        self.comment.content = 'x' * 256
        self._assert_comment_is_invalid()
    
    def test_get_replies(self):
        reply1 = PostComment.objects.create(author=self.user, post=self.post, content="Reply 1", parent=self.comment)
        reply2 = PostComment.objects.create(author=self.user, post=self.post, content="Reply 2", parent=self.comment)
        replies = self.comment.get_replies()
        self.assertIn(reply1, replies)
        self.assertIn(reply2, replies)
    
    def test_str_method(self):
        expected_str = f'Comment by {self.user.username} on {self.post.content}'
        self.assertEqual(str(self.comment), expected_str)

    def test_delete_post_deletes_comment(self):
        self.post.delete()
        with self.assertRaises(PostComment.DoesNotExist):
            PostComment.objects.get(pk=self.comment.pk)

    def test_delete_parent_comments_deletes_comment(self):
        child_comment = PostComment.objects.get(pk=2)
        self.assertEqual(child_comment.parent,self.comment)
        self.comment.delete()
        with self.assertRaises(PostComment.DoesNotExist):
            PostComment.objects.get(pk=child_comment.pk)
        
    def _assert_comment_is_valid(self):
        try:
            self.comment.full_clean()
        except (ValidationError):
            self.fail('Comment should be valid')

    def _assert_comment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.comment.full_clean()



