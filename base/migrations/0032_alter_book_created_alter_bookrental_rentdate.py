# Generated by Django 4.1.7 on 2023-05-20 02:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_alter_book_created_alter_bookrental_rentdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 2, 55, 10, 356101, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='bookrental',
            name='rentDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 2, 55, 10, 356101, tzinfo=datetime.timezone.utc)),
        ),
    ]
