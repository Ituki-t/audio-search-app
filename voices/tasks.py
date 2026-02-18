from celery import shared_task
from django.db import transaction
from .models import Voice
from .whisper_client import get_whisper_model
from .es_client import get_es

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

    model = get_whisper_model()

    result = model.transcribe(
        voice.audio_file.path,
        language="ja",
        fp16=False,
    )
    text = (result["text"] or "").strip()

    # text2es("voice_index", voice.id, text)

    try:
        es = get_es()
        es.index(
            index = "voice_index",
            id = voice.id,
            document = {
                "title": voice.title,
                "text": text,
                "voice_id": voice.id,
            },
            refresh = True, # インデックスに即座に反映させる
        )
        logger.info(f"Successfully indexed voice {voice.id}")
    except Exception:
        logger.exception(f"Failed to index voice {voice.id}")
        voice.transcribe_status = "failed"
        voice.save(update_fields=['transcribe_status'])
        raise

    voice.transcribe_status = "done"
    voice.save(update_fields=['transcribe_status'])
    return text


def text2es(index_name, voice_id, text):
    es = get_es()
    es.index(
        index = index_name,
        id = voice_id,
        document = {
            "text": text,
            "voice_id": voice_id,
        }
    )
