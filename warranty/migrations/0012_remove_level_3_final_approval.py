# Generated by Django 5.0.2 on 2024-09-28 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0011_alter_level_1_options_alter_level_2_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level_3',
            name='final_approval',
        ),
    ]
