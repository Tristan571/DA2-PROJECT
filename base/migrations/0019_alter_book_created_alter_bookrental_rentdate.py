# Generated by Django 4.1.7 on 2023-05-19 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_book_created_alter_bookrental_rentdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 22, 55, 44, 428284, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='bookrental',
            name='rentDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 19, 22, 55, 44, 428284, tzinfo=datetime.timezone.utc)),
        ),
    ]
