# Generated by Django 3.1.7 on 2021-04-05 23:05

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_remove_photo_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images', validators=[photos.models.validate_image]),
        ),
    ]
