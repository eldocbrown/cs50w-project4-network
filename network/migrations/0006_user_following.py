# Generated by Django 3.1.2 on 2020-11-05 16:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20201104_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
