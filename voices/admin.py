from django.contrib import admin
from .models import Voice
from .models import Segment

# Register your models here.


class VoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')

class SegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'voice', 'start_time', 'end_time', 'text')


admin.site.register(Voice, VoiceAdmin)
admin.site.register(Segment, SegmentAdmin)