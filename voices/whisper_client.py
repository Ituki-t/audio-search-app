import os


_model = None

def get_whisper_model():
    global _model
    if _model is None:
        import whisper # 遅延イイイポト
        model_name = os.getenv("WHISPER_MODEL", "base")
        _model = whisper.load_model(model_name)
    return _model
