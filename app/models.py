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
