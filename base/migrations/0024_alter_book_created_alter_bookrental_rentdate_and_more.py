# Generated by Django 4.1.7 on 2023-05-20 00:54

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_book_created_alter_bookrental_rentdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 0, 54, 24, 106957, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='bookrental',
            name='rentDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 0, 54, 24, 106957, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idCard',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator('^d{12}$', 'ID Card must be 12 digits long')]),
        ),
    ]