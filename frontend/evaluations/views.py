from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from .models import Evaluation_block, Evaluation
import re, unicodedata
import requests
import queue
import json

# input_text_regex = re.compile(r'^[\x20-\x7E\p{L}\p{N}]+$')
request_queue = queue.Queue()

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

        if validated_text.status_code == 503:
            request_queue.put((request, input_text, backend_url))
            return JsonResponse({"status" : 503})
        
        while not request_queue.empty():
            # Pokud je fronta neprázdná, převezměte request z fronty
            queued_request, queued_input_text, queued_backend_url = request_queue.get()
            queued_validated_text = requests.get(queued_backend_url, params={"text": queued_input_text})
            
            if queued_validated_text.status_code == 503:
                # Pokud je stále kód 503, přidejte request zpět na konec fronty
                request_queue.put((queued_request, queued_input_text, queued_backend_url))
                break
            else:
                # Pokud kód 503 není, zpracujte request
                queued_request_json = eval_fnc(queued_request, queued_input_text, queued_backend_url)
                if queued_request_json.status_code == 503:
                    # Pokud byl request opět přidán do fronty, přidejte ho zpět na konec fronty
                    request_queue.put((queued_request, queued_input_text, queued_backend_url))
                    break


        # * New Evaluation Block creation
        whole_claim = " ".join([claim["claim"] for claim in validated_text.json()])
        new_evaluation_block = Evaluation_block.objects.create(user=user, claims=whole_claim)

        for evaluation in validated_text.json():
            create_evaluation_fnc(new_evaluation_block, evaluation)

        return JsonResponse({"validated" : validated_text.json()})
        
    else:
        return HttpResponse(status=401)


# Create your views here.
def v1_dummy_fnc_backend_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    validated_text = requests.get("http://127.0.0.1:8002/backend/v1/dummy").json()

    return JsonResponse({"validated" : validated_text})

def v1_evaluation_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, "http://127.0.0.1:8002/backend/v1/eval")

def v1_evaluation_fast_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, "http://127.0.0.1:8002/backend/v1/eval_fast")


# ! RAG
def rag_dummy_fnc_backend_view(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    validated_text = requests.get("http://127.0.0.1:8002/backend/rag/dummy").json()

    return JsonResponse({"validated" : validated_text})

def rag_evaluation_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, "http://127.0.0.1:8002/backend/rag/eval")

def rag_evaluation_DPR_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, "http://127.0.0.1:8002/backend/rag/eval_DPR")
    
def rag_evaluation_Ada_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, "http://127.0.0.1:8002/backend/rag/eval_ada")

def rag_evaluation_BM25_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    text = data.get("text")
    return eval_fnc(request, text, "http://127.0.0.1:8002/backend/rag/eval_bm25")




