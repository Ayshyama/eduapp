from django.shortcuts import render

# Create your views here.
def userHome_page(request):
    return render(request, "home.html")