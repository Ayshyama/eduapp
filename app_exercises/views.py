from django.shortcuts import render
from django.views.generic import TemplateView


class ExerciseView(TemplateView):
    template_name = 'app_exercises/exercise.html'

