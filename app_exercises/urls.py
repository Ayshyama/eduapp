from django.urls import path

from app_exercises.views import ExerciseView, FinishExerciseView, NextExerciseView

urlpatterns = [
    path("<int:pk>/", ExerciseView.as_view(), name="exercise"),
    path("<int:pk>/next/", NextExerciseView.as_view(), name="next_exercise"),
    path("<int:pk>/finish/", FinishExerciseView.as_view(), name="finish_exercise"),
]