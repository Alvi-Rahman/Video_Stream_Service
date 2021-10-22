# Generated by Django 3.2.8 on 2021-10-22 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_stream_app', '0012_alter_videocontent_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videocontent',
            name='allowed_subscription',
        ),
        migrations.AddField(
            model_name='videocontent',
            name='allowed_subscription',
            field=models.ManyToManyField(null=True, related_name='subscription_type', to='video_stream_app.SubscriptionType'),
        ),
    ]