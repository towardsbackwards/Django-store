# Generated by Django 2.2.3 on 2019-07-06 09:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 8, 9, 18, 41, 169509, tzinfo=utc)),
        ),
    ]