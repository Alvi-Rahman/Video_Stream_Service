# Generated by Django 3.2.8 on 2021-10-21 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_stream_app', '0006_alter_subscription_subscription_validity'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubscriptionCategory',
            new_name='SubscriptionType',
        ),
    ]
