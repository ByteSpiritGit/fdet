from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
from .models import UserExtension
from django.contrib.auth.models import User, auth
import re
import requests


email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
username_regex = re.compile(r'^[\w.@+-]{1,150}$')
password_regex = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?!.*password)(?!.*12345678)(?!^\d+$)[A-Za-z\d.@$!%*?&^_-]{8,}$')

# Create your views here.
def registration_view(request, *args, **kwargs):
    first_name = request.GET["first_name"]
    last_name = request.GET["last_name"]
    email = request.GET["email"]
    username = request.GET["username"]
    password = request.GET["password"]
    password2 = request.GET["password2"]

    
    if not password_regex.search(password):
        # Password does not match the required regex pattern
        error_msg = "Password must contain at least 8 characters, 1 letter, 1 digit, and 1 special character. It cannot be too similar to your personal information and cannot be a commonly used password."
        return JsonResponse({"error_msg": error_msg})

    if not email_regex.search(email):
        # Email does not match the required regex pattern
        error_msg = "Email is not valid."
        return JsonResponse({"error_msg": error_msg})
    
    if not username_regex.search(username):
        # Username does not match the required regex pattern
        error_msg = "Username is not valid."
        return JsonResponse({"error_msg": error_msg})
    
    if password == password2:    
        if User.objects.filter(email=email).exists():
            error_msg = "Email already exists."
            return JsonResponse({"error_msg": error_msg})

        elif User.objects.filter(username=username).exists():
            error_msg = "Username already exists."
            return JsonResponse({"error_msg": error_msg})
            
        else:
            # Username and email do not exist
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            user_extension = UserExtension(user=user)
            user_extension.save()
            return JsonResponse({"success_msg": "User created successfully."})

    else:
        # Passwords do not match
        error_msg = "Passwords do not match."
        return JsonResponse({"error_msg": error_msg})


def login_view(request, *args, **kwargs):
    username = request.GET["username"]
    password = request.GET["password"]

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return JsonResponse({"success_msg": "User logged in successfully."})
    else:
        error_msg = "Invalid credentials."
        return JsonResponse({"error_msg": error_msg})

def authentication_view(request, *args, **kwargs):
    authentication = request.user.is_authenticated
    return JsonResponse({"authentication": authentication})

