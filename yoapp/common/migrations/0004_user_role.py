# Generated by Django 2.0.7 on 2018-07-31 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('CUSTOMER', 'CUSTOMER'), ('OWNER', 'OWNER'), ('MANAGER', 'MANAGER')], default='CUSTOMER', max_length=50),
        ),
    ]
