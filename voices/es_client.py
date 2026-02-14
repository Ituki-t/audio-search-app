import os
from elasticsearch import Elasticsearch

_es = None

def get_es():
    global _es
    if _es is None:
        _es = Elasticsearch(
                "http://" + os.getenv("ES_HOST", "elasticsearch") + ":" + os.getenv("ES_PORT", "9200")
                )
    return _es