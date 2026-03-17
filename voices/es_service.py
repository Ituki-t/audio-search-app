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


def search_docs_fulltext(query):
    es = get_es()
    query = {
        "query": {
            "match": {
                "text": query,
            }
        }
    }
    res = es.search(index=INDEX_NAME, body=query)
    results = get_voice_ids(res)
    return results


def get_voice_ids(res):
    results = []
    for hit in res["hits"]["hits"]:
        source = hit["_source"]
        results.append(source["voice_id"])
    return results