# Generated by Django 3.1.2 on 2020-11-21 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0008_auto_20201121_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='language',
        ),
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]