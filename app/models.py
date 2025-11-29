from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя с ролями"""

    ROLE_CHOICES = [
        ("user", "Пользователь"),
        ("psychologist", "Психолог"),
        ("admin", "Администратор"),
    ]

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="user", verbose_name="Роль"
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_psychologist(self):
        """Проверка, является ли пользователь психологом"""
        return self.role == "psychologist"

    def is_admin_user(self):
        """Проверка, является ли пользователь администратором"""
        return self.role == "admin" or self.is_superuser


class Application(models.Model):
    """Модель заявки на консультацию к психологу"""

    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("in_progress", "В работе"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Пользователь",
    )
    psychologist = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_applications",
        limit_choices_to={"role": "psychologist"},
        verbose_name="Психолог",
    )
    title = models.CharField(max_length=200, verbose_name="Тема")
    description = models.TextField(verbose_name="Описание проблемы")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"
