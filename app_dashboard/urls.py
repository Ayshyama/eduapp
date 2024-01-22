from django.urls import path
from .views import UserDashboardView

urlpatterns = [
    path('progress/', UserDashboardView.as_view(), name='user_progress'),
]
