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
    ConsultationForm,
    MeetingForm,
)
from .models import User, Application, FeedbackForm, Meeting


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


@login_required
def dashboard_student(request):
    """Панель управления для студентов"""
    if request.user.is_admin_user():
        return redirect("dashboard_admin")
    if request.user.is_psychologist():
        return redirect("dashboard_psychologist")
    
    applications = Application.objects.filter(user=request.user).order_by("-created_at")
    meetings = Meeting.objects.filter(student=request.user).order_by("date", "time")
    
    return render(
        request,
        "dashboard_student.html",
        {
            "applications": applications,
            "meetings": meetings,
        },
    )


@login_required
def dashboard_admin(request):
    """Панель управления для администраторов"""
    if not request.user.is_admin_user():
        return redirect("index")
    
    if request.method == "POST" and "change_role" in request.POST:
        user_id = request.POST.get("user_id")
        new_role = request.POST.get("role")
        if user_id and new_role:
            user = get_object_or_404(User, id=user_id)
            user.role = new_role
            user.save()
            messages.success(request, f"Роль пользователя {user.username} изменена на {user.get_role_display()}")
            return redirect("dashboard_admin")
    
    users = User.objects.all().order_by("-created_at")
    feedback_forms = FeedbackForm.objects.all().order_by("-created_at")
    
    return render(
        request,
        "dashboard_admin.html",
        {
            "users": users,
            "feedback_forms": feedback_forms,
        },
    )


@login_required
def dashboard_psychologist(request):
    """Панель управления для психологов"""
    if not request.user.is_psychologist():
        return redirect("index")
    
    applications = Application.objects.filter(
        psychologist=request.user
    ).order_by("-created_at")
    
    general_applications = Application.objects.filter(
        psychologist__isnull=True,
        status="pending"
    ).order_by("-created_at")
    
    meetings = Meeting.objects.filter(psychologist=request.user).order_by("date", "time")
    
    return render(
        request,
        "dashboard_psychologist.html",
        {
            "applications": applications,
            "general_applications": general_applications,
            "meetings": meetings,
        },
    )


@login_required
def application_detail_psychologist(request, application_id):
    """Детальный просмотр заявки для психолога"""
    if not request.user.is_psychologist():
        return redirect("index")
    
    application = get_object_or_404(Application, id=application_id)
    
    if application.psychologist and application.psychologist != request.user:
        messages.error(request, "У вас нет доступа к этой заявке.")
        return redirect("dashboard_psychologist")
    
    if request.method == "POST":
        if "take_application" in request.POST:
            if not application.psychologist:
                application.psychologist = request.user
                application.status = "in_progress"
                application.save()
                messages.success(request, "Заявка успешно взята в работу.")
                return redirect("application_detail_psychologist", application_id=application.id)
        elif "add_consultation" in request.POST:
            consultation_form = ConsultationForm(request.POST)
            if consultation_form.is_valid():
                consultation = consultation_form.save(commit=False)
                consultation.application = application
                consultation.psychologist = request.user
                consultation.save()
                if application.status == "pending":
                    application.status = "in_progress"
                    application.psychologist = request.user
                    application.save()
                messages.success(request, "Ответ успешно отправлен студенту.")
                return redirect("application_detail_psychologist", application_id=application.id)
        elif "add_meeting" in request.POST:
            meeting_form = MeetingForm(request.POST)
            if meeting_form.is_valid():
                meeting = meeting_form.save(commit=False)
                meeting.student = application.user
                meeting.psychologist = request.user
                meeting.application = application
                meeting.save()
                messages.success(request, "Встреча успешно назначена.")
                return redirect("application_detail_psychologist", application_id=application.id)
    else:
        consultation_form = ConsultationForm()
        meeting_form = MeetingForm()
    
    consultations = application.consultations.all().order_by("-created_at")
    
    return render(
        request,
        "application_detail_psychologist.html",
        {
            "application": application,
            "consultations": consultations,
            "consultation_form": consultation_form,
            "meeting_form": meeting_form,
        },
    )


@login_required
def application_detail_student(request, application_id):
    """Детальный просмотр заявки для студента"""
    if request.user.is_psychologist() or request.user.is_admin_user():
        return redirect("index")
    
    application = get_object_or_404(Application, id=application_id)
    
    if application.user != request.user:
        messages.error(request, "У вас нет доступа к этой заявке.")
        return redirect("dashboard")
    
    consultations = application.consultations.all().order_by("-created_at")
    
    return render(
        request,
        "application_detail_student.html",
        {
            "application": application,
            "consultations": consultations,
        },
    )
