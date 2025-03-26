from celery import shared_task
from django.core.cache import cache

@shared_task
def send_email(uid, content):
    cache.set(uid+'_emailed', content)
    return f"Email sent to {uid}"
