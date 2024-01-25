import random

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, RedirectView
from rest_framework.response import Response
from rest_framework.views import APIView

from app_accounts.models import UserProgress
from app_base.nav_menu import menu2
from app_exercises.gpt_utils import evaluate_code_with_chatgpt
from app_exercises.models import Exercise, Subject
from app_exercises.serializers import TestAnswerSerializer, CodeAnswerSerializer


class FinishExerciseView(DetailView):
    model = Subject
    template_name = 'app_exercises/finish.html'
    extra_context = {
        'title': 'Exercise',
        'menu': menu2,
        'menu_selected': 0,
    }


class ExerciseView(DetailView):
    model = Exercise
    template_name = 'app_exercises/exercise.html'
    extra_context = {
        'title': 'Exercise',
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

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        exercise = Exercise.objects.get(pk=self.kwargs['pk'])
        subject = exercise.lesson.module.subject

        exercises_done = UserProgress.objects.filter(user=user).values_list('exercise', flat=True)
        queryset = Exercise.objects.filter(lesson__module__subject=subject).exclude(pk__in=exercises_done)

        next_exercise = queryset.filter(pk__gt=exercise.pk).first()
        next_exercise = next_exercise if next_exercise else queryset.first()

        if next_exercise:
            return reverse('exercise', kwargs={'pk': next_exercise.pk})
        else:
            return reverse('finish_exercise', kwargs={'pk': subject.pk})


class SubmitBaseAPIView(APIView):
    def post(self, request, pk):
        exercise = Exercise.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            answer = serializer.validated_data['answer']
            result = self.check_answer(exercise, answer)

            if result['is_correct']:
                request.user.exercises_done.add(exercise)
            else:
                if request.user.life > 0:
                    request.user.life -= 1
                    request.user.save()

            result['user_life'] = request.user.life
            return Response(result)
        else:
            print(serializer.errors)
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
        # Chat logic will be here
        print("type(answer): ", type(answer))
        print("answer: ", answer, sep='\n')
        if random.randint(1, 5) == 1:
            return {'is_correct': True, 'message': 'You are right!'}
        else:
            return {'is_correct': False, 'message': 'You are wrong! Try again!'}