# Generated by Django 3.2 on 2021-09-29 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_remove_user_following'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]