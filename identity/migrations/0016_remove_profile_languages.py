# Generated by Django 3.1.4 on 2020-12-08 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0015_auto_20201208_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='languages',
        ),
    ]
