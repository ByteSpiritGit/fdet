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
        new_evaluation = Evaluation.objects.create(
            claim=evaluation["claim"], 
            label=evaluation["label"], 
            supports=evaluation["supports"], 
            refutes=evaluation["refutes"], 
            evidence=evaluation["evidence"]
        )
        evaluation["id"] = new_evaluation.id # ! Adding id to the obtained JSON -> passing to feedbacks app 

    context = {
        "validated" : validated_text
    }
    return JsonResponse(context)

def dummy_fnc_view(request):
    text = request.GET["text"]
    validated_text = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]

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
