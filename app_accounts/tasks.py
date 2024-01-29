from celery import shared_task
from django.db.models import F
from django.utils import timezone
from .models import CustomUser


@shared_task
def increment_user_life():
    CustomUser.objects.filter(life__lt=10).update(life=F('life') + 1)


@shared_task
def reset_day_streak():
    yesterday = timezone.now() - timezone.timedelta(days=1)
    users_to_reset = CustomUser.objects.exclude(
        exercises_done__userprogress__datetime__gte=yesterday
    )
    users_to_reset.update(day_streak=0)
