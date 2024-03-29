from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from .models import Evaluation_block, Evaluation
import re, unicodedata
import requests
import queue
import json
import time


# input_text_regex = re.compile(r'^[\x20-\x7E\p{L}\p{N}]+$')
# request_queue = queue.Queue()

# TODO:
# Move to settings.py or .env
backend_host = "http://172.18.0.2"
backend_port = "8002"
backend_base_url = backend_host + ":" + backend_port

def create_evaluation_fnc(evaluation_block, evaluation_dict):
    new_evaluation = Evaluation.objects.create(
        evaluation_block=evaluation_block,

        claim=evaluation_dict.get("claim"),
        label=evaluation_dict.get("label"), 
        supports=evaluation_dict.get("supports"), 
        refutes=evaluation_dict.get("refutes"),
        ei=evaluation_dict.get("ei"),
        nei=evaluation_dict.get("nei"),
        evidence=evaluation_dict.get("evidence"),
        justify=evaluation_dict.get("justify"),
        url=evaluation_dict.get("url")
    )
    evaluation_dict["id"] = new_evaluation.id # ! Adding id to the obtained JSON -> passing to feedbacks app
    evaluation_dict["evaluation_block"] = evaluation_block.id

def eval_fnc(request, input_text, backend_url):
    # # * Check for invalid characters
    # if not input_text_regex.match(input_text):
    #     return JsonResponse({"error_msg": "Invalid input. The input contains invalid characters.", "status": 400})
    # * Check for authentication
    user = request.user
    if user.is_authenticated:
        validated_text = requests.get(backend_url, params={"text" : input_text})

        while validated_text.status_code == 503:
            time.sleep(5)
            validated_text = requests.get(backend_url, params={"text" : input_text})

        try:
            # * New Evaluation Block creation
            whole_claim = " ".join([claim["claim"] for claim in validated_text.json()])
            new_evaluation_block = Evaluation_block.objects.create(user=user, claims=whole_claim)

            for evaluation in validated_text.json():
                create_evaluation_fnc(new_evaluation_block, evaluation)

            return JsonResponse({"validated" : validated_text.json()})

        except Exception as e:
            return HttpResponse(status=e)
        
    else:
        return HttpResponse(status=401)


# Create your views here.
# ! RAG
def rag_dummy_fnc_backend_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    validated_text = requests.get(f"{backend_base_url}/backend/rag/dummy").json()

    return JsonResponse({"validated" : validated_text})

def rag_evaluation_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, f"{backend_base_url}/backend/rag/eval")

def rag_evaluation_DPR_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, f"{backend_base_url}/backend/rag/eval_dpr")

def rag_evaluation_Ada_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, f"{backend_base_url}/backend/rag/eval_ada")

def rag_evaluation_BM25_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, f"{backend_base_url}/backend/rag/eval_bm25")




