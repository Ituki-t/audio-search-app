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
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 1,
                'cols': 40,
                'class': 'form-control mb-3',
                }),
        }