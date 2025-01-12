# Generated by Django 5.0.2 on 2024-10-05 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0027_generatedcode_assigned'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codegenerator',
            options={'verbose_name': 'تعداد', 'verbose_name_plural': 'تولید کد'},
        ),
        migrations.AlterModelOptions(
            name='generatedcode',
            options={'verbose_name': 'کد جدید', 'verbose_name_plural': 'کد های تولید شده'},
        ),
        migrations.AlterModelOptions(
            name='otp',
            options={'verbose_name': 'رمز یکبار مصرف', 'verbose_name_plural': 'رمز یکبار مصرف'},
        ),
        migrations.AlterField(
            model_name='codegenerator',
            name='number_of_codes',
            field=models.IntegerField(default=1, verbose_name='تعداد کد ها'),
        ),
        migrations.AlterField(
            model_name='generatedcode',
            name='assigned',
            field=models.BooleanField(default=False, verbose_name='اختصاص داده شده'),
        ),
        migrations.AlterField(
            model_name='generatedcode',
            name='code',
            field=models.CharField(max_length=6, unique=True, verbose_name='کد'),
        ),
        migrations.AlterField(
            model_name='generatedcode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تولید'),
        ),
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authenticate.generatedcode', verbose_name='کد'),
        ),
    ]