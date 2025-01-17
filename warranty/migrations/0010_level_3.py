# Generated by Django 5.0.2 on 2024-09-26 17:01

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0009_alter_level_1_date_alter_level_1_end_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Level_3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_approval', models.BooleanField(default=False, verbose_name='تایید نهایی')),
                ('submission_date', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ ثبت')),
                ('level1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='warranty.level_1')),
                ('level2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='warranty.level_2')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level3_submissions', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]
