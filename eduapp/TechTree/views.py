from django.shortcuts import render

# Create your views here.
def tech_tree(request):
    return render(request, "tech_tree.html")
