# Generated by Django 5.0.2 on 2024-09-22 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0003_alter_user_options_user_address_alter_user_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='شماره تماس'),
        ),
    ]