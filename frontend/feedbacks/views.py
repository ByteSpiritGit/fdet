from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Evaluation_Feedback
import requests

# Create your views here.
def eval_feedback_view(request, *args, **kwargs):
    feedback = request.GET["feedback"]
    eval_id = request.GET["eval_id"]

    Evaluation_Feedback.objects.create(feedback=feedback, evaluation=eval_id)


    return HttpResponse(status=402)