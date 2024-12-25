from datetime import timedelta

from django.conf import settings
from django.db.models import Q, F, QuerySet
from django.utils.timezone import now

MAX_MAILING_LIST_LENGTH = 5


class UserExtraQuerySet(QuerySet):
    def mailing_list(self):
        return self.filter(
            is_active=True, verified=True, subscribed=True,
        ).filter(
            Q(last_email_sent__isnull=True)
            | Q(last_email_sent__lt=now() - timedelta(seconds=settings.MAILING_LIST_INTERVAL))
        ).order_by(
            F("last_email_sent").asc(nulls_first=True)
        )[:MAX_MAILING_LIST_LENGTH]
