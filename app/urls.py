"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("support/", views.support, name="support"),
    path("feedback/", views.feedback, name="feedback"),
    path("faq/", views.faq, name="faq"),
    path("contacts/", views.contacts, name="contacts"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", views.dashboard_student, name="dashboard"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/psychologist/", views.dashboard_psychologist, name="dashboard_psychologist"),
    path("application/<int:application_id>/", views.application_detail_psychologist, name="application_detail_psychologist"),
    path("psychologists/", views.psychologists_list, name="psychologists_list"),
    path("application/create/", views.create_application, name="application_create"),
    path(
        "application/create/<int:psychologist_id>/",
        views.create_application,
        name="application_create_with_psychologist",
    ),
    path("my-applications/", views.my_applications, name="my_applications"),
]
