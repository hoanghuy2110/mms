# Generated by Django 3.0.5 on 2020-05-18 06:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200518_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='userskill',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
