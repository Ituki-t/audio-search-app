from django import forms
from .models import Voice
from .models import Segment


class UploadVoiceForm(forms.ModelForm):
    class Meta:
        model = Voice
        fields = ['audio_file']



class UpdateSegmentTextForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ['text']