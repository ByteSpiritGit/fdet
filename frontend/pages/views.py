from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests

# Create your views here.
def home_view(request, *args, **kwargs):
    models = {

    }
    return render(request, "base.html", models)


def evaluation_view(request, *args, **kwargs):
    text = request.GET["text"]
    validated_text = requests.get("http://127.0.0.1:8002/backend/eval", params={"text" : text}).json()

    context = {
        "validated" : validated_text
    }
    return JsonResponse(context)

def dummy_fnc_view(request):
    text = request.GET["text"]
    validated_text = [{"claim": "Dummy claim", "label" : 1, "supports" : 0.1457, "refutes" : 0.8543, "evidence" : "Dummy evidence"}]

    context = {
        "validated" : validated_text
    }
    return JsonResponse(context)

def dummy_fnc_backend_view(request):
    text = request.GET["text"]
    validated_text = requests.get("http://127.0.0.1:8002/backend/dummy").json()

    context = {
        "validated" : validated_text
    }
    return JsonResponse(context)
