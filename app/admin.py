from django.contrib import admin
from .models import User, Application, Consultation, FeedbackForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role", "phone", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["username", "email"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "psychologist", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "description"]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ["application", "psychologist", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["message"]


@admin.register(FeedbackForm)
class FeedbackFormAdmin(admin.ModelAdmin):
    list_display = ["subject", "name", "email", "status", "processed", "created_at"]
    list_filter = ["status", "processed", "created_at"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["created_at"]

