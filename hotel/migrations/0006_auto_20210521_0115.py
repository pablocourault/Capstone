# Generated by Django 3.2 on 2021-05-21 01:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='doubles',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(16)]),
        ),
        migrations.AddField(
            model_name='bookings',
            name='quadruples',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AddField(
            model_name='bookings',
            name='singles',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)]),
        ),
        migrations.AddField(
            model_name='bookings',
            name='triples',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)]),
        ),
    ]