from django.test import TestCase
from peer_support.models import Question, Response, User
from django.core.exceptions import ValidationError

class QuestionModelTest(TestCase):

    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json'
    ]

    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        test_question = Question.objects.create(
            author=self.user,
            title='Test Question',
            body='This is a test question.'
        )
        test_question.save()

    def test_valid_user(self):
            self._assert_user_is_valid()

    def test_question_creation(self):
        question = Question.objects.get(id=1)
        self.assertEqual(question.title, 'Test Question')
        self.assertEqual(question.body, 'This is a test question.')

    def test_get_responses(self):
        question = Question.objects.get(id=1)
        user = User.objects.get(username='@johndoe')
        response1 = Response.objects.create(user=user, question=question, body="Response 1")
        response2 = Response.objects.create(user=user, question=question, body="Response 2", parent=response1)
        responses = question.get_responses()
        self.assertIn(response1, responses)
        self.assertNotIn(response2, responses)

    def test_question_timestamps(self):
        question = Question.objects.get(id=1)
        self.assertIsNotNone(question.created_at)
        self.assertIsNotNone(question.updated_at)
        self.assertLessEqual(question.created_at, question.updated_at)

    def test_update_question(self):
        question = Question.objects.get(id=1)
        question.title = 'Updated Question Title'
        question.body = 'Updated question body.'
        question.save()
        updated_question = Question.objects.get(id=1)
        self.assertEqual(updated_question.title, 'Updated Question Title')
        self.assertEqual(updated_question.body, 'Updated question body.')

    def test_delete_question(self):
        question = Question.objects.get(id=1)
        question_id = question.id
        question.delete()
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=question_id)

    def test_question_string_representation(self):
        question = Question.objects.get(id=1)
        self.assertEqual(str(question), 'Test Question')

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()