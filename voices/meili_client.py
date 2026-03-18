import meilisearch
import os

_meili = None

def get_meili():
    global _meili
    if _meili is None:
        _meili = meilisearch.Client(
            'http://' + os.getenv('MEILI_HOST', 'meilisearch') + ':' + os.getenv('MEILI_PORT', '7700'),
            os.getenv('MEILI_MASTER_KEY')
        )
    return _meili