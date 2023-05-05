from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
import requests

# Create your views here.
def eval_feedback_view(request, *args, **kwargs):
    feedback = request.GET["feedback"]
    eval_block_id = request.GET["eval_block_id"]

    Evaluation_Feedback.objects.create(feedback=feedback, evaluation=eval_id)

    return HttpResponse(status=402)

def user_feedback_view(request, *args, **kwargs):
    feedback = request.GET["feedback"]
    user = request.user

    User_Feedback.objects.create(feedback=feedback, user=user)

    return HttpResponse(status=402)