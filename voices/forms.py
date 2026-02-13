from django import forms
from .models import Voice


class UploadVoiceForm(forms.ModelForm):
    class Meta:
        model = Voice
        fields = ['title', 'audio_file']