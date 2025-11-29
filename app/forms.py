from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import FeedbackForm, User, Application


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
            "psychologist": "Выберите психолога",
            "title": "Тема обращения",
            "description": "Описание проблемы",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["psychologist"].queryset = User.objects.filter(role="psychologist")
        self.fields["psychologist"].empty_label = "Выберите психолога"
