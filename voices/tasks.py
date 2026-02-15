from celery import shared_task
from django.db import transaction
from .models import Voice
from .whisper_client import get_whisper_model

@shared_task
def add(a, b):
    return a + b


@shared_task
def transcribe_voice(voice_id):
    voice = Voice.objects.get(id=voice_id)
    voice.transcribe_status = "running"
    voice.save(update_fields=['transcribe_status'])

    model = get_whisper_model()

    result = model.transcribe(
        voice.audio_file.path,
        language="ja",
        fp16=False,
    )
    text = (result["text"] or "").strip()

    with transaction.atomic(): # まあ無くたっていい
        voice.text = text
        voice.transcribe_status = "done"
        # voice.save(update_fields=['text', 'transcribe_status'])
    return text
