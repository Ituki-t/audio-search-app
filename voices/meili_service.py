from .meili_client import get_meili
import os
import dotenv
dotenv.load_dotenv()

audio_index = os.getenv('MEILI_AUDIO_INDEX', 'audio_index')

def add_audio_documents(segment):
    meili = get_meili()

    doc_id = segment.id
    voice = segment.voice
    docs = [{
        'id': doc_id,
        'title': voice.title,
        'text': segment.text,
        'start': segment.start_time,
        'end': segment.end_time,
        'voice_id': voice.id
    }]
    task = meili.index(audio_index).add_documents(docs)
    task_info = meili.wait_for_task(task.task_uid)
    print(task_info)

def search_audio_ids(query):
    meili = get_meili()
    results = meili.index(audio_index).search(query)
    hit_ids = []
    for hit in results['hits']:
        hit_ids.append(hit['voice_id'])
    return hit_ids

# use about `python manage.py shell`
def recreate_index():
    meili = get_meili()
    try:
        meili.index("audio_index").delete()
    except Exception:
        pass

    meili.create_index("audio_index", {"primaryKey": "id"})
    return "Index recreated"