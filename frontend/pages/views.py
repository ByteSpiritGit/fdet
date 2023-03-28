from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests

# Create your views here.
def home_view(request, *args, **kwargs):
    models = {

    }
    return render(request, "base.html", models)

