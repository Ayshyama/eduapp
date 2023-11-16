from django.test import TestCase
from django.utils import timezone

from app_accounts.models import CustomUser, UserExerciseConversation, UserStatistic, UserProgress
from app_exercises.models import Subject, Module, Lesson, Exercise, Keywords, TestAnswer


class ModelCreationTestCase(TestCase):

    lesson = None
    module = None
    subject = None
    keyword = None
    exercise = None
    user = None
    progress = None

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject = Subject.objects.create(name='Mathematics', description='Study of numbers')
        cls.module = Module.objects.create(name='Algebra',
                                           description='About algebra',
                                           subject=cls.subject)
        cls.lesson = Lesson.objects.create(name='Quadratic Equations',
                                           description='Introduction to Quadratic Equations',
                                           module=cls.module)
        cls.exercise = Exercise.objects.create(name='Solve Quadratic Equations x^2 - 5x + 6 = 0',
                                               lesson=cls.lesson,
                                               is_test=True)
        cls.keyword = Keywords.objects.create(keyword='quadratic')
        cls.exercise.keywords.add(cls.keyword)
        cls.test_answer = TestAnswer.objects.create(name='x=2 and x=3',
                                                    exercise=cls.exercise,
                                                    is_correct=True)

        cls.user = CustomUser.objects.create_user(username='john', email='john@example.com', password='123')
        cls.conversation = UserExerciseConversation.objects.create(user=cls.user, exercise=cls.exercise,
                                                                   message='Hello', is_human=True)

        cls.statistic = UserStatistic.objects.create(user=cls.user, progress=UserProgress.objects.count())

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, 'Mathematics')
        self.assertEqual(self.subject.description, 'Study of numbers')

    def test_module_creation(self):
        self.assertEqual(self.module.name, 'Algebra')
        self.assertEqual(self.module.subject, self.subject)

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.name, 'Quadratic Equations')
        self.assertEqual(self.lesson.module, self.module)

    def test_exercise_creation(self):
        self.assertEqual(self.exercise.name, 'Solve Quadratic Equations x^2 - 5x + 6 = 0')
        self.assertEqual(self.exercise.lesson, self.lesson)
        self.assertTrue(self.exercise.is_test)

    def test_keywords_association(self):
        self.assertIn(self.keyword, self.exercise.keywords.all())

    def test_test_answer_creation(self):
        self.assertEqual(self.test_answer.name, 'x=2 and x=3')
        self.assertEqual(self.test_answer.exercise, self.exercise)
        self.assertTrue(self.test_answer.is_correct)

    def test_custom_user_creation(self):
        self.assertEqual(self.user.username, 'john')
        self.assertEqual(self.user.email, 'john@example.com')
        self.assertEqual(self.user.life, 10)
        self.assertEqual(self.user.day_streak, 0)

    def test_user_exercise_conversation_creation(self):
        self.assertEqual(self.conversation.user, self.user)
        self.assertEqual(self.conversation.exercise, self.exercise)
        self.assertEqual(self.conversation.message, 'Hello')
        self.assertTrue(self.conversation.is_human)

    def test_user_progress_auto_creation(self):
        # Assume user and exercise have been created in setUpTestData
        self.user.exercises_done.add(self.exercise)

        # Now check if a UserProgress instance was created
        progress_exists = UserProgress.objects.filter(user=self.user, exercise=self.exercise).exists()
        self.assertTrue(progress_exists,
                        "UserProgress instance was not created when an exercise was added to exercises_done.")

