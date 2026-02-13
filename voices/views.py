from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Voice
from .forms import UploadVoiceForm


# Create your views here.

def index(request):
    voice = Voice.objects.all()
    return render(request, 'voices/index.html', {'voice': voice})


def upload(request):
    if request.method == 'POST':
        form = UploadVoiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('voices:index')
    else:
        form = UploadVoiceForm()
    return render(request, 'voices/upload.html', {'form': form})