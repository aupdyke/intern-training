"""
URL configuration for detection_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from detections import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from detections.views import AppView


urlpatterns = [
    path('', AppView.as_view(), name = 'frontend'),
    path('admin/', admin.site.urls),
    path("api/stats/", include("detections.urls")),
    path('video_feed/', views.video_feed, name = 'video_feed')
] #+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
