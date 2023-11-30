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

from pages.views import *
from evaluations.views import *
from feedbacks.views import *
from userExtensions.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # *Pages
    path('', home_view, name="home"),
    path('about_us', about_us_view, name="about_us"),
    path('evalOutput', evalOutput, name="eval_output"),
    path('users/register', registerPage, name="register_age"),
    path('users/login', loginPage, name="login_page"),
    path('csrf_view', csrf_view, name="csrf_view"),

    # *User Extensions
    path('registration', registration_view, name="registration"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('authentication', authentication_view, name="authentication"),

    # *Evaluations
    # RAG
    path('rag/dummy_backend', rag_dummy_fnc_backend_view, name="rag_dummy_backend"),
    path('rag/eval', rag_evaluation_view, name="rag_evaluation"),
    path('rag/eval_DPR', rag_evaluation_DPR_view, name="rag_evaluation_DPR"),
    path('rag/eval_ada', rag_evaluation_Ada_view, name="rag_evaluation_Ada"),
    path('rag/eval_bm25', rag_evaluation_BM25_view, name="rag_evaluation_BM25"),
    
    # *Feedbacks
    path('eval_feedback', eval_feedback_view, name="feedback"),
    path('user_feedback', user_feedback_view, name="user_feedback"),
]