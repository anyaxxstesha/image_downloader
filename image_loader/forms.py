from django.forms import ModelForm

from image_loader.models import Image


class ImageUploadForm(ModelForm):
    """Upload Image Form."""
    class Meta:
        model = Image
        fields = ('image', )