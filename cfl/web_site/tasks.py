from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from web_site.models import Challenge


@shared_task
def delete_old_posts():
    now = timezone.now()
    time_threshold = now - timedelta(days=7)  # Установите желаемый порог времени для удаления постов
    old_posts = Challenge.objects.filter(created_at__lte=time_threshold)
    old_posts.delete()
