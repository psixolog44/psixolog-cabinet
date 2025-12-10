from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from .models import FeedbackForm, User, Application, Consultation, Meeting


class FeedbackFormForm(forms.ModelForm):
    class Meta:
        model = FeedbackForm
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Ваш email"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тема сообщения"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваше сообщение",
                    "rows": 6,
                }
            ),
        }
        labels = {
            "name": "Имя",
            "email": "Email",
            "subject": "Тема",
            "message": "Сообщение",
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        label="Email",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя пользователя"}
            ),
        }
        labels = {
            "username": "Имя пользователя",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Подтверждение пароля"}
        )
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = "user"
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя пользователя"}
        ),
        label="Имя пользователя",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
        label="Пароль",
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Неверное имя пользователя или пароль")
            if not user.is_active:
                raise forms.ValidationError("Этот аккаунт неактивен")
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Фамилия"}
            ),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def clean_first_name(self):
        """Очистка поля first_name - преобразует пустую строку в None"""
        first_name = self.cleaned_data.get("first_name")
        return first_name.strip() if first_name else ""

    def clean_last_name(self):
        """Очистка поля last_name - преобразует пустую строку в None"""
        last_name = self.cleaned_data.get("last_name")
        return last_name.strip() if last_name else ""


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Текущий пароль"}
        ),
        label="Текущий пароль",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Новый пароль"}
        ),
        label="Новый пароль",
        min_length=8,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Подтверждение нового пароля",
            }
        ),
        label="Подтверждение нового пароля",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Неверный текущий пароль")
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("Пароли не совпадают")
        return new_password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ApplicationForm(forms.ModelForm):
    """Форма для подачи заявки психологу"""

    class Meta:
        model = Application
        fields = ["psychologist", "title", "description"]
        widgets = {
            "psychologist": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тема обращения"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Опишите вашу ситуацию или проблему",
                    "rows": 8,
                }
            ),
        }
        labels = {
            "psychologist": "Выберите психолога (необязательно)",
            "title": "Тема обращения",
            "description": "Описание проблемы",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["psychologist"].queryset = User.objects.filter(role="psychologist")
        self.fields["psychologist"].required = False
        self.fields["psychologist"].empty_label = "Не выбирать"

        def label_from_instance(obj):
            if obj.first_name or obj.last_name:
                return f"{obj.first_name} {obj.last_name}".strip()
            return obj.username

        self.fields["psychologist"].label_from_instance = label_from_instance


class ConsultationForm(forms.ModelForm):
    """Форма для ответа психолога на заявку"""

    class Meta:
        model = Consultation
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваш ответ студенту",
                    "rows": 6,
                }
            ),
        }
        labels = {
            "message": "Ответ",
        }


class MeetingForm(forms.ModelForm):
    """Форма для назначения встречи"""

    class Meta:
        model = Meeting
        fields = ["date", "time"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "class": "form-control date-input",
                    "type": "date",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "class": "form-control time-input",
                    "type": "time",
                }
            ),
        }
        labels = {
            "date": "Дата встречи",
            "time": "Время встречи",
        }

    def __init__(self, *args, psychologist=None, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        self.psychologist = psychologist

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        psychologist = self.psychologist

        if not date or not time or not psychologist:
            return cleaned_data

        meeting_datetime = datetime.combine(date, time)

        conflicting_meetings = Meeting.objects.filter(
            psychologist=psychologist, date=date, time=time
        )

        if self.instance and self.instance.pk:
            conflicting_meetings = conflicting_meetings.exclude(pk=self.instance.pk)

        if conflicting_meetings.exists():
            raise forms.ValidationError(
                "На это время уже назначена встреча. Пожалуйста, выберите другое время."
            )

        nearby_meetings = Meeting.objects.filter(
            psychologist=psychologist, date=date
        ).exclude(time=time)

        if self.instance and self.instance.pk:
            nearby_meetings = nearby_meetings.exclude(pk=self.instance.pk)

        for meeting in nearby_meetings:
            meeting_datetime_obj = datetime.combine(meeting.date, meeting.time)
            time_diff = abs(
                (meeting_datetime - meeting_datetime_obj).total_seconds() / 60
            )

            if time_diff < 30:
                raise forms.ValidationError(
                    f"Между встречами должен быть интервал минимум 30 минут. "
                    f"У вас уже есть встреча {meeting.date.strftime('%d.%m.%Y')} в {meeting.time.strftime('%H:%M')}."
                )

        return cleaned_data
