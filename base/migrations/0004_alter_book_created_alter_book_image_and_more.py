# Generated by Django 4.1.7 on 2023-05-17 16:22

import base.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_book_created_alter_book_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 17, 16, 22, 28, 779156, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='static\\errorimg\\errorimg.png', upload_to=base.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='bookrental',
            name='rentDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 17, 16, 22, 28, 781160, tzinfo=datetime.timezone.utc)),
        ),
    ]
