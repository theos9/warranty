# Generated by Django 5.0.2 on 2024-09-23 23:50

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0007_alter_level_1_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='level_1',
            name='end_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]