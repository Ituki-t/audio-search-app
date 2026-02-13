from django import forms
from .models import Voice


class UploadVoiceForm(forms.ModelForm):
    class Meta:
        model = Voice
        fields = ['audio_file']