# Generated by Django 3.2 on 2021-09-24 22:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20210924_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='_network_user_following_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
