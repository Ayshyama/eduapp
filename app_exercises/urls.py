from django.urls import path

from app_exercises.views import ExerciseView

urlpatterns = [
    path("", ExerciseView.as_view(), name="exercise"),
]