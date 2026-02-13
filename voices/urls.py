from django.urls import path

from . import views

app_name = 'voices'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('download/<int:voice_id>/', views.download, name='download'),
    # path('voice/<int:voice_id>/', views.voice_detail, name='voice_detail'),
]