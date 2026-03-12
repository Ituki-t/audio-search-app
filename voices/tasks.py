from celery import shared_task
from .models import Voice
from .models import Segment

from .whisper_service import transcribe_audio_file
from .whisper_service import save_whisper_segment
from .meili_service import add_audio_documents

import logging
logger = logging.getLogger(__name__)

@shared_task
def add(a, b):
    return a + b


@shared_task
def transcribe_voice(voice_id):
    voice = Voice.objects.get(id=voice_id)
    voice.transcribe_status = "running"
    voice.save(update_fields=['transcribe_status'])

    segments = transcribe_audio_file(voice.audio_file.path)
    for segment in segments:
        seg = save_whisper_segment(voice, segment)
        add_audio_documents(seg)

    voice.transcribe_status = "done"
    voice.save(update_fields=['transcribe_status'])
    return segments
