# Generated by Django 2.2.4 on 2019-08-30 09:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_auto_20190830_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 1, 9, 27, 1, 297383, tzinfo=utc)),
        ),
    ]
