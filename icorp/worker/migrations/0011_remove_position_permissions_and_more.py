# Generated by Django 4.2.9 on 2024-07-21 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0010_rename_birth_date_profile_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='permissions',
        ),
        migrations.AddField(
            model_name='position',
            name='access',
            field=models.ManyToManyField(blank=True, related_name='positions', to='worker.accessgroup', verbose_name='Разрешения'),
        ),
        migrations.CreateModel(
            name='ProfileAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to='worker.accessgroup')),
                ('profile_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_set', to='worker.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='access',
            field=models.ManyToManyField(blank=True, related_name='profiles', through='worker.ProfileAccess', to='worker.accessgroup', verbose_name='Разрешения'),
        ),
    ]