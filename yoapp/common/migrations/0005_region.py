# Generated by Django 2.0.7 on 2018-07-31 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=200)),
            ],
        ),
    ]
