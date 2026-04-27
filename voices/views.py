from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import os

from django.http import FileResponse
from .models import Voice
from .models import Segment
from .forms import UploadVoiceForm
from .forms import UpdateSegmentTextForm
from .tasks import transcribe_voice
from .tasks import update_audio_document
from .meili_service import search_audio_ids
from .meili_service import search_audio_segments_by_meili
from .es_service import search_docs_fulltext
from .es_service import search_doc_by_es

import logging
logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    query = request.GET.get('text_query')
    engine_query = request.GET.get('search_engine')
    voices = []
    voice_datas = []
    if query:
        if engine_query == "elasticsearch":
            # voice_ids = search_docs_fulltext(query)
            segs = search_doc_by_es(query)
            voice_datas = build_voice_datas(segs)
            print("voice_datas is ", voice_datas)
        elif engine_query == "meilisearch":
            # voice_ids = search_audio_ids(query)
            segs = search_audio_segments_by_meili(query)
            voice_datas = build_voice_datas(segs)
            print("voice_datas is ", voice_datas)
        else:
            # voice_ids = search_docs_fulltext(query) # DEFAULT: es
            segs = search_doc_by_es(query)
            voice_datas = build_voice_datas(segs)
            print("voice_datas is ", voice_datas)
    else:
        voices = Voice.objects.all().order_by('-uploaded_at')

    context = {
        'voices': voices,
        'voice_datas': voice_datas,
        'query': query,
    }
    return render(request, 'voices/index.html', context)


def build_voice_datas(segments):
    voice_ids = [seg['voice_id'] for seg in segments]
    voices = Voice.objects.in_bulk(voice_ids)

    rows = []
    for seg in segments:
        voice = voices.get(seg['voice_id'])
        if voice:
            rows.append({
                'voice': voice,
                'start_time': seg['start_time'],
                'end_time': seg['end_time'],
            })
    return rows


def upload(request):
    if request.method == 'POST':
        form = UploadVoiceForm(request.POST, request.FILES)
        if form.is_valid():
            voice = form.save(commit=False)
            title = request.FILES['audio_file'].name
            voice.title = title
            voice.save()
            transcribe_voice.delay(voice.id)
            return redirect('voices:index')
    else:
        form = UploadVoiceForm()
    return render(request, 'voices/upload.html', {'form': form})


def download(request, voice_id):
    voice = get_object_or_404(Voice, pk=voice_id)
    res = FileResponse(
        open(voice.audio_file.path, 'rb'),
        as_attachment=True,
        filename=os.path.basename(voice.audio_file.name)
    )
    return res


def delete(request, voice_id):
    if request.method == 'POST':
        voice = get_object_or_404(Voice, pk=voice_id)
        voice.delete()
        return redirect('voices:index')
    else:
        return render(request, 'voices/confirm_delete.html', {'voice_id': voice_id})


def detail(request, voice_id):
    voice = get_object_or_404(Voice, pk=voice_id)
    segments = Segment.objects.filter(voice=voice).order_by("id") # start_timeでソートしてもいい
    start_time = request.GET.get('start_time')

    context = {
        'voice': voice,
        'segments': segments,
    }
    if start_time:
        context['start_time'] = start_time

    return render(request, 'voices/detail.html', context)


def update_segment_text(request, voice_id, segment_id):
    voice = get_object_or_404(Voice, pk=voice_id)
    segments = Segment.objects.filter(voice=voice)
    for seg in segments:
        segment = get_object_or_404(Segment, pk=seg.id, voice=voice)

        if request.method == 'POST':
            form = UpdateSegmentTextForm(request.POST, instance=segment)
            if form.is_valid():
                form.save()
                update_audio_document.delay(segment.id)
                return redirect('voices:detail', voice_id=voice_id)
        else:
            form = UpdateSegmentTextForm(instance=segment)

    context = {
        'form': form,
        'voice': voice,
        'segment': segment,
    }
    return render(request, 'voices/update_text.html', context)