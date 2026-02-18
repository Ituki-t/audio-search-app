from .es_client import get_es
import os

import dotenv
dotenv.load_dotenv()

import logging
logger = logging.getLogger(__name__)

INDEX_NAME = os.getenv("ES_INDEX", "voice_index")


def index_voice(voice, text):

    try:
        es = get_es()
        es.index(
            index = INDEX_NAME,
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
