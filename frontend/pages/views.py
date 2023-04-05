from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):

    models = {

    }
    return render(request, "index.html", models)


def old_eval_view(request, *args, **kwargs):

    models = {

    }
    return render(request, "./pages/oldEval.html", models)
