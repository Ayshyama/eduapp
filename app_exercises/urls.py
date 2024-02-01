from django.urls import path
from . import views
from app_exercises.views import ExerciseView, FinishExerciseView, NextExerciseView, SubmitTestAPIView, SubmitCodeAPIView


urlpatterns = [
    path("<int:pk>/", ExerciseView.as_view(), name="exercise"),
    path("<int:pk>/next/", NextExerciseView.as_view(), name="next_exercise"),
    path("<int:pk>/finish/", FinishExerciseView.as_view(), name="finish_exercise"),
    path("api/submit_test/<int:pk>/", SubmitTestAPIView.as_view(), name="submit_test"),
    path("api/submit_code/<int:pk>/", SubmitCodeAPIView.as_view(), name="submit_code"),
    path("api/create-room/<str:uuid>/", views.create_room, name="create_room"),
]