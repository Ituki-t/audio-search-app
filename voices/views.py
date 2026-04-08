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
from .es_service import search_docs_fulltext
from .es_service import search_doc_by_es

import logging
logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    query = request.GET.get('text_query')
    engine_query = request.GET.get('search_engine')

    if query:
        if engine_query == "elasticsearch":
            # voice_ids = search_docs_fulltext(query)
            segs = search_doc_by_es(query)
            voice_ids = []
            voice_segments = []
            for seg in segs:
                voice_id = seg['voice_id']
                voice_ids.append(voice_id)
                voice_segments.append({
                    "voice_id": voice_id,
                    "start_time": seg['start_time'],
                    "end_time": seg['end_time'],
                })
        elif engine_query == "meilisearch":
            voice_ids = search_audio_ids(query)
        else:
            voice_ids = search_docs_fulltext(query) # DEFAULT: es
        voices = Voice.objects.filter(id__in=voice_ids)
    else:
        voices = Voice.objects.all()
        segs = Segment.objects.all()
        voice_segments = []
        for seg in segs:
            voice_segments.append({
                "voice_id": seg.voice.id,
                "start_time": seg.start_time,
                "end_time": seg.end_time,
            })

    context = {
        'voices': voices,
        'voice_segments': voice_segments,
    }
    return render(request, 'voices/index.html', context)


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
    context = {
        'voice': voice,
        'segments': segments,
    }
    return render(request, 'voices/detail.html', context)


def update_segment_text(request, voice_id, segment_id):
    voice = get_object_or_404(Voice, pk=voice_id)
    segment = get_object_or_404(Segment, pk=segment_id, voice=voice)
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