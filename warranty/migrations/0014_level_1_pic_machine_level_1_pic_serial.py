# Generated by Django 5.0.2 on 2024-10-05 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0013_level_1_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='level_1',
            name='pic_machine',
            field=models.ImageField(blank=True, null=True, upload_to='data/machine/', verbose_name='تصویر دستگاه'),
        ),
        migrations.AddField(
            model_name='level_1',
            name='pic_serial',
            field=models.ImageField(blank=True, null=True, upload_to='data/serial/', verbose_name='تصویر سریال'),
        ),
    ]
