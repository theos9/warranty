# Generated by Django 5.0.2 on 2024-09-22 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0005_alter_user_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='level_1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.IntegerField(choices=[(1, 'چرخ خیاطی'), (2, 'اتو پرس'), (3, 'اتو مخزن دار')], default=0)),
                ('model', models.CharField(max_length=255)),
                ('serial', models.CharField(max_length=255)),
            ],
        ),
    ]
