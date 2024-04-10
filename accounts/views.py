from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        newUser = User(username = username, email = email)
        print (newUser)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)
        messages.info(request, "Successful Registration")
        print ("registered")
        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "login.html", context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Username or password is invalid")
            return render(request, "login.html", context)

        messages.success(request, "Successfully login")
        login(request, user)
        return redirect("index")
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully Logout")
    return redirect("index")