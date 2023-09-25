from django.urls import path
from .views import support

urlpatterns = [
    path('', support, name='support'),
]