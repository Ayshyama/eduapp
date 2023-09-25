from django.urls import path
from .views import tech_tree

urlpatterns = [
    path('', tech_tree, name='tech_tree'),
]



