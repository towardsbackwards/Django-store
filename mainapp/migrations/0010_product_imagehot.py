# Generated by Django 2.2.4 on 2019-09-03 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20190903_0338'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imageHot',
            field=models.ImageField(blank=True, null=True, upload_to='products_hot', verbose_name='Картинка должна быть 1366х800 px'),
        ),
    ]