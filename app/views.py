from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    FeedbackFormForm,
    RegisterForm,
    LoginForm,
    ProfileForm,
    PasswordChangeForm,
    ApplicationForm,
)
from .models import User, Application


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
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            from django.contrib.auth import authenticate

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get("next", "index")
                return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def profile_view(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль успешно обновлен.")
                return redirect("profile")
        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Пароль успешно изменен.")
                return redirect("profile")

    return render(
        request,
        "profile.html",
        {"profile_form": profile_form, "password_form": password_form},
    )


@login_required
def create_application(request, psychologist_id=None):
    """Создание заявки психологу"""
    if request.user.is_psychologist():
        messages.error(
            request,
            "Психологи не могут подавать заявки. Используйте панель управления для работы с заявками.",
        )
        return redirect("index")
    
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.status = "pending"
            application.save()
            messages.success(
                request,
                "Заявка успешно отправлена! Психолог рассмотрит её в ближайшее время.",
            )
            return redirect("my_applications")
    else:
        form = ApplicationForm()
        if psychologist_id:
            psychologist = get_object_or_404(
                User, id=psychologist_id, role="psychologist"
            )
            form.fields["psychologist"].initial = psychologist
    
    return render(request, "application_create.html", {"form": form})


@login_required
def my_applications(request):
    """Список заявок текущего пользователя"""
    applications = Application.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return render(
        request,
        "my_applications.html",
        {"applications": applications},
    )


def psychologists_list(request):
    """Список всех психологов"""
    psychologists = User.objects.filter(role="psychologist").order_by("username")
    return render(
        request,
        "psychologists_list.html",
        {"psychologists": psychologists},
    )
