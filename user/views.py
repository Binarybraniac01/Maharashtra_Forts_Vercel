from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *

import uuid


# @login_required(login_url="/login-page/")

def register_page(request):

    if request.method == "POST":
        data = request.POST

        raw_email = data.get("email")
        email = raw_email.lower()
        raw_username = data.get("username")
        username = raw_username.strip()
        raw_password = data.get("password")
        password = raw_password.strip()

        if User.objects.filter(email=email).exists():
            messages.info(request, "email already exists. Please use valid email...")
            return redirect('/register-page/')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists. Please use another username...")
            return redirect('/register-page/')

        user = User.objects.create(email=email, username=username)
        
        user.set_password(password)
        user.save()
        # messages.info(request, "User registration successfull. You can LOG IN now !")
        # return redirect('/login-page/')
        login(request, user)
        return redirect('/')

    return render(request, "register.html", context={"page": "Register"})



def login_page(request):

    if request.method == "POST":
        data = request.POST

        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username...")
            return redirect('/login-page/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Password...")
            return redirect('/login-page/')
        else:
            login(request, user)
            return redirect("/")

    return render(request, "login.html", context={"page": "Login"})


@login_required(login_url="/login-page/")
def logout_view(request):
    logout(request)
    return redirect('/login-page/')


def guest_acc(request):

    username = uuid.uuid4()
    password = str(uuid.uuid4())

    user = User.objects.create(username=username)    
    user.set_password(password)
    user.save()

    login(request, user)
    return redirect("/")
