from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.UserLoginView.as_view(), name='account_login'),
    path('signup/', views.UserSignupView.as_view(), name='account_signup'),
]
