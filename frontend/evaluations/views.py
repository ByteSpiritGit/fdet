from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
from .models import Evaluation_block, Evaluation
import requests
from django.middleware.csrf import get_token

# Create your views here.
def evaluation_view(request, *args, **kwargs):
    text = request.GET["text"]

    validated_text = requests.get("http://127.0.0.1:8002/backend/v1/eval", params={"text" : text}).json()
    
    # //print(type(validated_text[0]["label"]))

    # * New Evaluation Block creation
    whole_claim = " ".join([claim["claim"] for claim in validated_text])
    new_evaluation_block = Evaluation_block.objects.create(claims=whole_claim)

    for evaluation in validated_text:
        new_evaluation = Evaluation.objects.create(
            evaluation_block=new_evaluation_block,

            claim=evaluation.get("claim"),
            label=evaluation.get("label"), 
            supports=evaluation.get("supports"), 
            refutes=evaluation.get("refutes"),
            ei=evaluation.get("ei"),
            nei=evaluation.get("nei"),
            evidence=evaluation.get("evidence")
        )
        evaluation["id"] = new_evaluation.id # ! Adding id to the obtained JSON -> passing to feedbacks app
        evaluation["evaluation_block"] = new_evaluation_block.id

    return JsonResponse({"validated" : validated_text})


def evaluation_fast_view(request, *args, **kwargs):
    text = request.GET["text"]

    validated_text = requests.get("http://127.0.0.1:8002/backend/v1/eval_fast", params={"text" : text}).json()
    
    # * New Evaluation Block creation
    whole_claim = " ".join([claim["claim"] for claim in validated_text])
    new_evaluation_block = Evaluation_block.objects.create(claims=whole_claim)

    for evaluation in validated_text:
        new_evaluation = Evaluation.objects.create(
            evaluation_block=new_evaluation_block,

            claim=evaluation.get("claim"),
            label=evaluation.get("label"), 
            supports=evaluation.get("supports"), 
            refutes=evaluation.get("refutes"),
            ei=evaluation.get("ei"),
            nei=evaluation.get("nei"),
            evidence=evaluation.get("evidence")
        )
        evaluation["id"] = new_evaluation.id
        evaluation["evaluation_block"] = new_evaluation_block.id

    return JsonResponse({"validated" : validated_text})


def dummy_fnc_view(request):
    text = request.GET["text"]
    validated_text = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "ei": 0.0005, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]

    context = {
        "validated" : validated_text
    }
    return JsonResponse(context)

def dummy_fnc_backend_view(request):
    text = request.GET["text"]
    validated_text = requests.get("http://127.0.0.1:8002/backend/v1/dummy").json()

    return JsonResponse({"validated" : validated_text})


# ! RAG
def rag_evaluation_view(request, *args, **kwargs):
    text = request.GET["text"]

    validated_text = requests.get("http://127.0.0.1:8002/backend/rag/eval", params={"text" : text}).json()

    # * New Evaluation Block creation
    whole_claim = " ".join([claim["claim"] for claim in validated_text])
    new_evaluation_block = Evaluation_block.objects.create(claims=whole_claim)

    for evaluation in validated_text:
        new_evaluation = Evaluation.objects.create(
            evaluation_block=new_evaluation_block,

            claim=evaluation.get("claim"),
            label=evaluation.get("label"), 
            supports=evaluation.get("supports"), 
            refutes=evaluation.get("refutes"),
            ei=evaluation.get("ei"),
            nei=evaluation.get("nei"),
            evidence=evaluation.get("evidence"),
            justify=evaluation.get("justify")
        )
        evaluation["id"] = new_evaluation.id # ! Adding id to the obtained JSON -> passing to feedbacks app
        evaluation["evaluation_block"] = new_evaluation_block.id

    return JsonResponse({"validated" : validated_text})

def rag_dummy_fnc_backend_view(request):
    text = request.GET["text"]
    validated_text = requests.get("http://127.0.0.1:8002/backend/rag/dummy").json()

    return JsonResponse({"validated" : validated_text})



def csrf_view(request):
    return JsonResponse({"csrf_token": get_token(request)})