from django.urls import path
from .views import UserDashboardProgressView, user_progress_json, UserDashboardView

urlpatterns = [
    path('', UserDashboardView.as_view(), name='user_dashboard'),
    path('<slug:slug>/progress/', UserDashboardProgressView.as_view(), name='user_progress'),
    path('json/user-progress/', user_progress_json, name='user_progress_json'),
]
