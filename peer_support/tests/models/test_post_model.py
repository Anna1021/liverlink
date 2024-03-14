"""Unit tests for the post model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from peer_support.models import Post, PostComment, User

class PostModelTestCase(TestCase):
    """Unit tests for the post model"""

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/default_post.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.post = Post.objects.get(pk=1)

    def test_valid_post(self):
        self._assert_post_is_valid()
    
    def test_correct_author(self):
        self.assertEqual(self.post.author,self.user)

    def test_correct_text(self):
        self.assertEqual(self.post.text,"User post")

    def test_timestamp(self):
        self.assertIsNotNone(self.post.created_at)

    def test_text_must_not_be_empty(self):
        self.post.text = ""
        self._assert_post_is_invalid()

    def test_text_must_not_contain_more_than_280_characters(self):
        self.post.text = 'x' * 281
        self._assert_post_is_invalid()

    def test_correct_visibility(self):
        self.assertEqual(self.post.visibility,"G")
    
    def test_delete_post(self):
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=self.post.pk)
        
    def test_comment_belongs_to_a_post(self):
        post1 = Post.objects.create(author=self.user, text="Post 1")
        comment1 = PostComment.objects.create(author=self.user, post=post1, content="Comment 1") 
        comments = post1.get_comments()
        self.assertIn(comment1, comments)
        self.assertEqual(comments.count(), 1) 

    def test_comment_does_not_belong_to_a_post(self):
        post1 = Post.objects.create(author=self.user, text="Post1")
        post2 = Post.objects.create(author=self.user, text="Post2")
        comment3 = PostComment.objects.create(author=self.user, post=post2, content="Comment 3") 
        comments = post1.get_comments()
        self.assertNotIn(comment3, comments) 

    def test_reply_to_comment_is_not_a_comment_of_post(self):
        post1 = Post.objects.create(author=self.user, text="Post 1")
        comment1 = PostComment.objects.create(author=self.user, post=post1, content="Comment 1")
        comment2 = PostComment.objects.create(author=self.user, post=post1, content="Comment 2", parent=comment1)
        comments = post1.get_comments()
        self.assertNotIn(comment2, comments)
    
    def _assert_post_is_valid(self):
        try:
            self.post.full_clean()
        except (ValidationError):
            self.fail('Post should be valid')

    def _assert_post_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.post.full_clean()
