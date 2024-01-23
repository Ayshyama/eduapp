from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, RedirectView
from rest_framework.response import Response
from rest_framework.views import APIView

from app_base.nav_menu import menu2
from app_exercises.models import Exercise, TestAnswer, Subject


class FinishExerciseView(DetailView):
    model = Subject
    template_name = 'app_exercises/finish.html'


class ExerciseView(DetailView):
    model = Exercise
    template_name = 'app_exercises/exercise.html'
    extra_context = {  # Need to pass these 3 context variables to each inherited from base.html template
        'title': 'EDU APP',
        'menu': menu2,
        'menu_selected': 0,
    }

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


class SubmitTestAPIView(APIView):
    def post(self, request, pk):
        print(request.data)
        return Response({'result': 'success, you submitted the test!'})


class SubmitCodeAPIView(APIView):
    def post(self, request, pk):
        print(request.data)
        return Response({'result': 'success, you submitted the code!'})

