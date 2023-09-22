from django.urls import path, include
from .views import userHome_page

urlpatterns = [
    path('', userHome_page, name='home'),
    path('TechTree', include('TechTree.urls')),
    path('exercises', include('exercises.urls')),
    path('challanges', include('challanges.urls')),
    path('comunity', include('comunity.urls')),
    path('user_profile', include('user_profile.urls')),
    path('support', include('support.urls')),
]

