from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render
from .models import UserExtension
from django.contrib.auth.models import User, auth
import re
import json

email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
password_regex = re.compile(r'((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$')
username_regex = re.compile(r'^[a-zA-Z0-9.\-+]{3,150}$')

# Create your views here.
def registration_view(request, *args, **kwargs):
    
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password2 = data.get("password2")

    
    if not password_regex.search(password):
        # Password does not match the required regex pattern
        error_msg = """
            One uppercase letter (A-Z)<br />
            Two lowercase letters (a-z)<br />
            One digit (0-9)<br />
            One special character (e.g. !@#$%^&*)<br />
            Be at least 5 characters long
        """
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
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            user_extension = UserExtension(user=user)
            user_extension.save()
            auth.login(request, user)
            return JsonResponse({ "success_msg": "User created successfully.", "status": 200, "username": username })
    else:
        # Passwords do not match
        error_msg = "Passwords do not match."
        return JsonResponse({"error_msg": error_msg, "status": 400})


def login_view(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
   
    username_email = data.get("username_email")
    password = data.get("password")

    if "@" in username_email:
        try:
            user = User.objects.get(email=username_email)
            username_email = user.username
        except User.DoesNotExist:
            user = None
    else:
        user = auth.authenticate(username=username_email, password=password)


    if user is not None:
        auth.login(request, user)
        return JsonResponse({
            "success_msg": "User logged in successfully.",
            "username": user.username,
        })
    else:
        error_msg = "Invalid credentials."
        return JsonResponse({"error_msg": error_msg, "status": 400})

def authentication_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return JsonResponse({"username": request.user.username})
    else:
        return HttpResponse(status=401)

def logout_view(request, *args, **kwargs):
    auth.logout(request)
    return JsonResponse({"success_msg": "User logged out successfully."})