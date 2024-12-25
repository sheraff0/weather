from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserExtraQuerySet


class User(AbstractUser):
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False, verbose_name="Подтвержден Email")
    subscribed = models.BooleanField(default=False, verbose_name="Подписан на рассылку")
    last_email_sent = models.DateTimeField(null=True, blank=True, verbose_name="Последняя рассылка")

    extra = UserExtraQuerySet.as_manager()

    def __str__(self):
        return f"{self.username} ({self.email})"
