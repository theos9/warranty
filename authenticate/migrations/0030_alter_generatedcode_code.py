# Generated by Django 5.0.2 on 2024-10-07 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0029_generatedcode_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedcode',
            name='code',
            field=models.CharField(max_length=8, unique=True, verbose_name='کد'),
        ),
    ]
