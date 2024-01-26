from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.UserLoginView.as_view(), name='user_login'),
    path('signup/', views.UserSignupView.as_view(), name='user_signup'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]
