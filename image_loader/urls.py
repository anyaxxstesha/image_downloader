from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from image_loader.apps import ImageLoaderConfig
from image_loader.views import UploadImageView

app_name = ImageLoaderConfig.name

urlpatterns = [
    path('image/upload', csrf_exempt(UploadImageView.as_view()), name='image_upload'),
]