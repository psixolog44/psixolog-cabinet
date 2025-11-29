from django import forms
from .models import FeedbackForm


class FeedbackFormForm(forms.ModelForm):
    class Meta:
        model = FeedbackForm
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Ваш email"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Тема сообщения"}),
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": "Ваше сообщение", "rows": 6}),
        }
        labels = {
            "name": "Имя",
            "email": "Email",
            "subject": "Тема",
            "message": "Сообщение",
        }

