"""Unit tests for the Response model."""
from django.test import TestCase
from peer_support.models import Question, Response, User
from django.core.exceptions import ValidationError


class ResponseModelTestCase(TestCase):
    """Unit tests for the Response model."""
    
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json',
        'peer_support/tests/fixtures/default_question.json',
        'peer_support/tests/fixtures/default_response.json',   
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_response_content(self):
        response = Response.objects.get(id=1)
        expected_user = response.user
        expected_body = response.body
        self.assertEquals(expected_user.username, '@johndoe')
        self.assertEquals(expected_body, 'This is a sample response body.')

    def test_get_responses(self):
        test_user = User.objects.get(username='@johndoe')
        test_question = Question.objects.get(title='Sample Question Title')
        parent_response = Response.objects.create(
            user=test_user,
            question=test_question,
            body='This is a parent response.'
        )
        child_response = Response.objects.create(
            user=test_user,
            question=test_question,
            parent=parent_response,
            body='This is a child response.'
        )
        responses = parent_response.get_responses()
        self.assertIn(child_response, responses)

    def test_response_deletion(self):
        response = Response.objects.get(body='This is a sample response body.')
        response_id = response.id
        response.delete()
        with self.assertRaises(Response.DoesNotExist):
            Response.objects.get(id=response_id)

    def test_response_creation(self):
        test_question = Question.objects.get(title='Sample Question Title')
        response = Response.objects.create(
            user=self.user,
            question=test_question,
            body='New test response.'
        )
        self.assertEqual(response.body, 'New test response.')

    def test_response_update(self):
        response = Response.objects.get(body='This is a sample response body.')
        response.body = 'Updated response'
        response.save()
        updated_response = Response.objects.get(id=response.id)
        self.assertEqual(updated_response.body, 'Updated response')

    def test_response_relationships(self):
        response = Response.objects.get(body='This is a sample response body.')
        self.assertEqual(response.user.username, '@johndoe')
        self.assertEqual(response.question.title, 'Sample Question Title')

    def test_response_timestamps(self):
        response = Response.objects.get(body='This is a sample response body.')
        self.assertIsNotNone(response.created_at)
        self.assertIsNotNone(response.updated_at)
        self.assertLessEqual(response.created_at, response.updated_at)

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
