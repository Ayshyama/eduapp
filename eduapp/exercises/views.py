from django.shortcuts import render

# Create your views here.
def exercises(request):
    return render(request, "exercises.html")