# Generated by Django 3.2.8 on 2021-10-23 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_stream_app', '0016_userpayments'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayments',
            name='card_no',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='userpayments',
            name='mfs_channel',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]