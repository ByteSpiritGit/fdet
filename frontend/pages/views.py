from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
import requests


# Create your views here.


def home_view(request, *args, **kwargs):
    models = {}
    return render(request, "./index.html", models)

def evalOutput(request, *args, **kwargs):
    models = {}
    return render(request, "./pages/evalOutput.html", models)

def registerPage(request, *args, **kwargs):
    return render(request, "./pages/register.html", {})

def loginPage(request, *args, **kwargs):
    return render(request, "./pages/login.html", {})

def csrf_view(request):
    return JsonResponse({"csrf_token": get_token(request)})