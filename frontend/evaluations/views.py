from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
from .models import Evaluation
import requests
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def evaluation_view(request, *args, **kwargs):
    text = request.GET["text"]


    # text_list = text.split(". ")
    # i = 0
    # dicts_list = []
    # index_dict = {}
    # for sentence in text_list:
    #     database_dict = {
    #         "claim" : none,
    #         "label" : none,
    #         "supports" : none,
    #         "refutes" : none,
    #         "evidence" : none,
    #         "id" : none
    #     }
    #     index_dict[i] = sentence
    #     evaluated_sentence = Evaluation.objects.get(claim=sentence)
    #     if evaluated_sentence:
    #         database_dict["claim"] = evaluated_sentence.claim
    #         database_dict["label"] = evaluated_sentence.label
    #         database_dict["supports"] = evaluated_sentence.supports
    #         database_dict["refutes"] = evaluated_sentence.refutes
    #         database_dict["evidence"] = evaluated_sentence.evidence
    #         database_dict["id"] = evaluated_sentence.id
    #         dicts_list.append(database_dict)
    #     i += 1
    #     text_list.remove(sentence)

    # text_back = ". ".join()

    validated_text = requests.get("http://127.0.0.1:8002/backend/eval", params={"text" : text}).json()
    # print(type(validated_text[0]["label"]))

    for evaluation in validated_text:
        if Evaluation.objects.filter(claim=evaluation["claim"]).exists():
            Evaluation.objects.filter(claim=evaluation["claim"]).update(
                label=evaluation["label"], 
                supports=evaluation["supports"], 
                refutes=evaluation["refutes"], 
                evidence=evaluation["evidence"]
            )
        else:
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


def csrf_view(request):
    return JsonResponse({"csrf_token": get_token(request)})