from django.db import models
from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError

# Create your models here.

ACTION_CHOICES = (
    ('NO_FILTER', 'no filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert'),
    ('BOX_BLUR', 'box_blur'),
    ('EMBOSS', 'emboss'),
    ('IDENTITY', 'identity'),
    ('HIGHPASS', 'highpass'),
    ('SHARPEN', 'sharpen'),
)


def validate_image(image):
    file_size = image.file.size
    # limit_kb = 150
    # if file_size > limit_kb * 1024:
    #     raise ValidationError("Max size of file is %s KB" % limit)

    limit_mb = 15
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)


class Photo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', validators=[validate_image])
    created = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):

        # Open Image
        pil_img = Image.open(self.image)

        # Convert the image to array and do some processing
        cv_img = np.array(pil_img)

        img = get_filtered_image(cv_img, self.action)

        # Convert back to pil Image
        im_pil = Image.fromarray(img)

        # save
        buffer = BytesIO()

        im_pil = im_pil.convert("L")
        im_pil.save(buffer, format='JPEG')

        image_png = buffer.getvalue()

        self.image.save(str(self.image), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)
