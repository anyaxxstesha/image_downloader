from django.db import models

# Create your models here.


class Image(models.Model):
    """Image database model."""
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="media/images/",
    )
    permanent_link = models.URLField(
        verbose_name="Постоянная ссылка"
    )
