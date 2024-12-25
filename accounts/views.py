from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import (
    login_required,
    LoginView as LoginViewBase,
    LogoutView as LogoutViewBase,
)
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse

from common.utils.jwt import jwt_encode, jwt_decode
from .forms import RegisterForm


class LoginView(LoginViewBase):
    template_name = "login.html"
    next_page = "home"


class LogoutView(LogoutViewBase):
    template_name = "home.html"
    next_page = "home"


def send_verification_email(request, email):
    token = jwt_encode({"email": email}, timeout=300)
    url = request.build_absolute_uri(
        reverse("verify_email", kwargs={"token": token}))
    message = f"Пожалуйста, перейдите по ссылке для подтверждения email: {url}"
    html_message = f"""Пожалуйста, перейдите по <a href="{url}">ссылке</a> для подтверждения email."""
    send_mail("WEATHER - код подтверждения", message, settings.EMAIL_HOST_USER, [email],
              html_message=html_message)


def sign_up(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": RegisterForm()})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()
            send_verification_email(request, user.email)
            return render(request, "register.html", {"form": None, "email": user.email})
        else:
            return render(request, "register.html", {"form": form})


def verify_email(request, **kwargs):
    context = {"notification": "Ссылка недействительна"}
    token = kwargs.get("token")
    if payload := jwt_decode(token):
        if email := payload.get("email"):
            if user := get_user_model().objects.filter(email=email).first():
                user.is_active = True
                user.verified = True
                user.save()
                login(request, user)
                context = {"notification": "Поздравляем! Вы авторизованы."}
    return render(request,"home.html", context=context)

def subscription_action(request, status: bool):
    user = request.user
    user.subscribed = status
    user.save()
    return redirect("home")


@login_required
def subscribe(request):
    return subscription_action(request, True)


@login_required
def unsubscribe(request):
    return subscription_action(request, False)
