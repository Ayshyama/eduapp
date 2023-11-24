from django.urls import path
from . import views

urlpatterns = [
    path('loginn/', views.UserLoginView.as_view(), name='account_login'),
    path('signupp/', views.UserSignupView.as_view(), name='account_signup'),
]
