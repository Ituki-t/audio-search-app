from django.db import models

# Create your models here.

class Voice(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='voices/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    transcribe_status = models.CharField(
        max_length=20,
        default="pending" # pending/running/done/failed
        )
    def __str__(self):
        return self.title