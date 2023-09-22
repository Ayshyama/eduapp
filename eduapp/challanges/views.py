from django.shortcuts import render

# Create your views here.
def challanges(request):
    return render(request, "challanges.html")