"""fDetAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages.views import home_view, old_eval_view, evalOutput
from evaluations.views import *
from feedbacks.views import eval_feedback_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # *Pages
    path('', home_view, name="home"),
    path('oldEval', old_eval_view, name="old_eval"),
    path('evalOutput', evalOutput, name="eval_output"),

    # *Evaluations
    path('csrf_view', csrf_view, name="csrf_view"),
    # V1
    path('evaluation', evaluation_view, name="evaluation"),
    path('evaluation_fast', evaluation_fast_view, name="evaluation_fast"),
    path('dummy', dummy_fnc_view, name="dummy"),
    path('dummy_backend', dummy_fnc_backend_view, name="dummy_backend"),
    # RAG
    path('rag_evaluation', rag_evaluation_view, name="rag_evaluation"),
    path('rag_dummy_backend', rag_dummy_fnc_backend_view, name="rag_dummy_backend"),
    
    
    # *Feedbacks
    path('eval_feedback', eval_feedback_view, name="feedback"),
]
