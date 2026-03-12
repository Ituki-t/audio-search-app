from .models import Segment

from .whisper_client import get_whisper_model


def transcribe_audio_file(path):
    model = get_whisper_model()

    result = model.transcribe(
        path,
        language="ja",
        fp16=False,
    )
    return get_audio_segments(result)

def get_audio_segments(result):
    segments = []
    for segment in result.get("segments", []):
        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
        })
    return segments

def save_whisper_segment(voice, segment):
    seg = Segment(
        voice=voice,
        start_time=segment['start'],
        end_time=segment['end'],
        text=segment['text']
    )
    seg.save()
    return seg