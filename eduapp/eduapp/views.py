from django.http import HttpResponse
from django.shortcuts import render, redirect


def landing_page(request):
    return render(request, "landing_page.html")

def signIn_page(request):
    return render(request, "signIn_page.html")

def signUp_page(request):
    return render(request, "registration_page.html")

def restorePass_page(request):
    return render(request, "restore_password.html")

def userHome_page(request):
    return render(request, "home.html")

