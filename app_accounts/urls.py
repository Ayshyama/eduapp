from django.urls import path
from . import views

urlpatterns = [
    path('signinn/', views.UserLoginView.as_view(), name='account_login'),
    path('signupp/', views.UserSignupView.as_view(), name='account_signup'),
]
