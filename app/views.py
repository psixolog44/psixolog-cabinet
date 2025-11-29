from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import FeedbackFormForm, RegisterForm, LoginForm


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def faq(request):
    return render(request, "faq.html")


def contacts(request):
    return render(request, "contacts.html")


def services(request):
    return render(request, "services.html")


def support(request):
    return render(request, "support.html")


def feedback(request):
    if request.method == "POST":
        form = FeedbackFormForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.",
            )
            return redirect("feedback")
    else:
        form = FeedbackFormForm()
    return render(request, "feedback.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Добро пожаловать, {user.username}! Вы успешно зарегистрированы.",
            )
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
