# Generated by Django 3.2 on 2021-06-06 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0011_comments_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='message',
            field=models.CharField(default='Service request received', max_length=512),
        ),
    ]