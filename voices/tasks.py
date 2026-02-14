from celery import shared_task
from .models import Voice

@shared_task
def add(a, b):
    return a + b