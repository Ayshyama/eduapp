from django.urls import path
from .views import comunity

urlpatterns = [
    path('', comunity, name='comunity'),
]
