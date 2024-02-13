from django.test import TestCase
from django.urls import reverse
from peer_support.models import Question
from django.utils import timezone
from peer_support.models import User


class ResourcesViewTest(TestCase):
    fixtures = [
        'peer_support/tests/fixtures/default_user.json',
        'peer_support/tests/fixtures/other_users.json'
    ]

    @classmethod
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

        number_of_questions = 5
        for question_num in range(number_of_questions):
            Question.objects.create(
                title=f'Question {question_num}',
                body='This is a test question body.',
                created_at=timezone.now() - timezone.timedelta(days=question_num),
                author=self.user
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/resources/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('resources'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources.html')

    def test_pagination_is_correct(self):
        response = self.client.get(reverse('resources'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('questions' in response.context)
        self.assertEqual(len(response.context['questions']), 5)

    def test_questions_ordered_by_created_at(self):
        response = self.client.get(reverse('resources'))
        self.assertEqual(response.status_code, 200)
        questions = response.context['questions']
        self.assertTrue(all(questions[i].created_at >= questions[i + 1].created_at for i in range(len(questions) - 1)))
