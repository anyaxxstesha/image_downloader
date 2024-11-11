import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from image_loader.forms import ImageUploadForm
from image_loader.models import Image


# Create your views here.


class UploadImageView(CreateView):
    """Image upload image view."""
    model = Image
    form_class = ImageUploadForm
    api_mode = False
    context_object_name = 'uploaded_image'
    success_url = 'http://localhost:8000/image/upload'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        content_type = self.request.headers.get('Content-Type')
        # print(form_kwargs.get('files', {}).get('image', self).__dict__)
        if form_kwargs.get('files', {}).get('image') is None:
            if content_type is not None and content_type.startswith('image/'):
                self.api_mode = True
                file_object = io.BytesIO(self.request.body)
                file_type = content_type.split('/')[-1]
                file_name = f"image.{file_type}"
                form_kwargs['files']['image'] = InMemoryUploadedFile(
                    file_object,
                    'image',
                    file_name,
                    content_type.split('/')[1],
                    len(self.request.body),
                    None
                )

        return form_kwargs

    def get_success_url(self):
        if self.api_mode:
            return ''
        return super().get_success_url()

    def form_invalid(self, form):
        if self.api_mode:
            return JsonResponse(form.errors.get_json_data(), status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.api_mode:
            return JsonResponse({'permanent_link': self.object.image.name})
        return HttpResponseRedirect(self.get_success_url())

    def render_to_response(self, context, **response_kwargs):
        if self.api_mode:
            uploaded_image = context.get('uploaded_image')
            return JsonResponse({'permanent_link': uploaded_image.permanent_link})
        return super().render_to_response(context, **response_kwargs)
