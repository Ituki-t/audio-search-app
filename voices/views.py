from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import os

from django.http import FileResponse
from .models import Voice
from .forms import UploadVoiceForm
from .tasks import transcribe_voice
from .tasks import text2es


# Create your views here.

def index(request):
    voice = Voice.objects.all()
    return render(request, 'voices/index.html', {'voice': voice})


def upload(request):
    if request.method == 'POST':
        form = UploadVoiceForm(request.POST, request.FILES)
        if form.is_valid():
            voice = form.save(commit=False)
            title = request.FILES['audio_file'].name
            voice.title = title
            voice.save()
            transcribe_voice.delay(voice.id)
            # text2es("voice_index", voice.id, transcribe)
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