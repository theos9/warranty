# Generated by Django 5.0.2 on 2024-10-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0024_codegenerator'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
