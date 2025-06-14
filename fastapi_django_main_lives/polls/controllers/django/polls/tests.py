from django.test import TestCase
from .models import Question

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)