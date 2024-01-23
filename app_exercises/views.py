import random

from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, RedirectView
from rest_framework.response import Response
from rest_framework.views import APIView

from app_base.nav_menu import menu2
from app_exercises.models import Exercise, TestAnswer, Subject
from app_exercises.serializers import TestAnswerSerializer, CodeAnswerSerializer


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


class SubmitBaseAPIView(APIView):
    def post(self, request, pk):
        exercise = Exercise.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            answer = serializer.validated_data['answer']
            result = self.check_answer(exercise, answer)

            if result['is_correct']:
                request.user.exercises_done.add(exercise)
                if request.user.life < 10:
                    request.user.life += 1
            else:
                if request.user.life > 0:
                    request.user.life -= 1

            request.user.save()
            result['user_life'] = request.user.life
            return Response(result)
        else:
            return Response(serializer.errors, status=400)

    def get_serializer(self, data):
        raise NotImplementedError

    def check_answer(self, exercise, answer):
        raise NotImplementedError


class SubmitTestAPIView(SubmitBaseAPIView):
    def get_serializer(self, data):
        return TestAnswerSerializer(data=data)

    def check_answer(self, exercise, answer):
        exercise_set = set((item.id, item.is_correct) for item in exercise.testanswer_set.all())
        answer_set = set((int(key[12:]), val) for key, val in answer.items())
        if exercise_set == answer_set:
            return {'is_correct': True, 'message': 'You are right!'}
        elif len(exercise_set.difference(answer_set)) == 1:
            return {'is_correct': False, 'message': 'You are almost right! Try again!'}
        else:
            return {'is_correct': False, 'message': 'You are wrong! Try again!'}


class SubmitCodeAPIView(SubmitBaseAPIView):
    def get_serializer(self, data):
        return CodeAnswerSerializer(data=data)

    def check_answer(self, exercise, answer):
        if random.randint(1, 5) == 1:
            return {'is_correct': True, 'message': 'You are right!'}
        else:
            return {'is_correct': False, 'message': 'You are wrong! Try again!'}
