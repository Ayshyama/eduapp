from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, RedirectView

from app_exercises.models import Exercise, TestAnswer, Subject


class FinishExerciseView(DetailView):
    model = Subject
    template_name = 'app_exercises/finish.html'


class ExerciseView(DetailView):
    model = Exercise
    template_name = 'app_exercises/exercise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise = context['object']
        context['is_done'] = exercise.userprogress_set.filter(user=self.request.user).exists()
        context['questions'] = exercise.testanswer_set.all()
        context['keywords'] = exercise.keywords.all()
        return context


class NextExerciseView(RedirectView):
    permanent = True
    pattern_name = 'exercise'



