# Generated by Django 3.2.8 on 2021-10-23 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video_stream_app', '0015_videocontent_cover_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPayments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_method', models.CharField(blank=True, choices=[('VISA', 'Visa'), ('MASTERCARD', 'Mastercard'), ('ANEX', 'Amex'), ('MFS', 'MFS')], max_length=100, null=True)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
