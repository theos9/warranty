# Generated by Django 5.0.2 on 2024-09-23 14:48

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0004_alter_level_1_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level_1',
            name='date',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
    ]
