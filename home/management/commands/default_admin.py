from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Заполнение списка городов"

    def handle(self, *args, **options):
        DEFAULT_ADMIN = dict(
            username="weather-admin",
            password="Weather!@#123",
            email="radimir.shevchenko@gmail.com",
            is_superuser=True,
            is_staff=True,
            verified=True,
            subscribed=True,
        )

        User = get_user_model()
        if User.objects.filter(username=DEFAULT_ADMIN["username"]).exists():
            return
        password = DEFAULT_ADMIN.pop("password")
        user = User.objects.create(**DEFAULT_ADMIN)
        user.set_password(password)
        user.save()
