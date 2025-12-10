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

    def get_display_name(self):
        """Возвращает имя и фамилию, если они есть, иначе username"""
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        if full_name:
            return full_name
        return self.username or ""


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


class Consultation(models.Model):
    """Модель консультации/ответа психолога на заявку"""

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="consultations",
        verbose_name="Заявка",
    )
    psychologist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="consultations",
        limit_choices_to={"role": "psychologist"},
        verbose_name="Психолог",
    )
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Консультация по заявке {self.application.id}"


class FeedbackForm(models.Model):
    """Модель формы обратной связи"""

    STATUS_CHOICES = [
        ("new", "Новое"),
        ("read", "Прочитано"),
        ("replied", "Отвечено"),
        ("archived", "Архивировано"),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.name} ({self.email})"


class Meeting(models.Model):
    """Модель встречи/консультации между студентом и психологом"""
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_meetings",
        limit_choices_to={"role": "user"},
        verbose_name="Студент",
    )
    psychologist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="psychologist_meetings",
        limit_choices_to={"role": "psychologist"},
        verbose_name="Психолог",
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meetings",
        verbose_name="Заявка",
    )
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"
        ordering = ["date", "time"]
    
    def __str__(self):
        return f"Встреча {self.student.username} с {self.psychologist.username} - {self.date} {self.time}"