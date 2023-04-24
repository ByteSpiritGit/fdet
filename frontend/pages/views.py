from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    models = { }
    return render(request, "index.html", models)

def evalOutput(request, *args, **kwargs):
    models = { }
    return render(request, "./pages/evalOutput.html", models)


def loginPage(request, *args, **kwargs):
    models = {}
    return render(request, "./pages/login.html", models)


def registerPage(request, *args, **kwargs):
    models = {}
    return render(request, "./pages/register.html", models)