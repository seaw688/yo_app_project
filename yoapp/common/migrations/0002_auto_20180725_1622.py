# Generated by Django 2.0.7 on 2018-07-25 16:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created_date',
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date joined'),
            preserve_default=False,
        ),
    ]