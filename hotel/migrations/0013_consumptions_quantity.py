# Generated by Django 3.2 on 2021-06-07 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0012_services_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumptions',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
