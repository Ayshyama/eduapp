from django.urls import path
from .views import UserDashboardView, user_progress_json

urlpatterns = [
    path('progress/', UserDashboardView.as_view(), name='user_progress'),
    path('user-progress-json/', user_progress_json, name='user_progress_json'),
]
