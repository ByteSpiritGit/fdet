from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Evaluation
import requests

# Create your views here.
def evaluation_view(request, *args, **kwargs):
    text = request.GET["text"]
    validated_text = requests.get("http://127.0.0.1:8002/backend/eval", params={"text" : text}).json()
    # print(type(validated_text[0]["label"]))

    for evaluation in validated_text:
        Evaluation.objects.create(claim=evaluation["claim"], label=evaluation["label"], supports=evaluation["supports"], refutes=evaluation["refutes"], evidence=evaluation["evidence"])

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
