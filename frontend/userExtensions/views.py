from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
from .models import UserExtension
from django.contrib.auth.models import User, auth
import re
import requests
import json

email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
username_regex = re.compile(r'^[\w.@+-]{1,150}$')
password_regex = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?!.*password)(?!.*12345678)(?!^\d+$)[A-Za-z\d.@$!%*?&^_-]{8,}$')

# Create your views here.
def registration_view(request, *args, **kwargs):
    
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password2 = data.get("password2")

    
    if not password_regex.search(password):
        # Password does not match the required regex pattern
        error_msg = "Password must contain at least 8 characters, 1 letter, 1 digit, and 1 special character. It cannot be too similar to your personal information and cannot be a commonly used password."
        return JsonResponse({"error_msg": error_msg, "status": 400})

    if not email_regex.search(email):
        # Email does not match the required regex pattern
        error_msg = "Email is not valid."
        return JsonResponse({"error_msg": error_msg, "status": 400})
    
    if not username_regex.search(username):
        # Username does not match the required regex pattern
        error_msg = "Username is not valid."
        return JsonResponse({"error_msg": error_msg, "status":400})
    
    if password == password2:    
        if User.objects.filter(email=email).exists():
            error_msg = "Email already exists."
            return JsonResponse({"error_msg": error_msg, "status":409})

        elif User.objects.filter(username=username).exists():
            error_msg = "Username already exists."
            return JsonResponse({"error_msg": error_msg, "status":409})
            
        else:
            # Everything is valid
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            user_extension = UserExtension(user=user)
            user_extension.save()
            return JsonResponse({"success_msg": "User created successfully.", "status": 200})

    else:
        # Passwords do not match
        error_msg = "Passwords do not match."
        return JsonResponse({"error_msg": error_msg, "status": 400})


def login_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
   
    username = data.get("username")
    password = data.get("password")

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

