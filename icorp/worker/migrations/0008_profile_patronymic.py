# Generated by Django 4.2.9 on 2024-07-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0007_profile_data_start_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Отчество'),
        ),
    ]
