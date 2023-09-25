from django.urls import path
from .views import challanges

urlpatterns = [
    path('', challanges, name='challanges'),
]
