from django.urls import path
from . import views
from detections.views import AppView

urlpatterns = [
    path('log/', views.detection_stats, name = 'detection_stats')
]