# Generated by Django 3.2 on 2021-05-18 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_guests_rates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=64)),
                ('roomtype', models.CharField(max_length=1)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('quantity', models.IntegerField(max_length=2)),
            ],
        ),
        migrations.DeleteModel(
            name='Rates',
        ),
    ]
