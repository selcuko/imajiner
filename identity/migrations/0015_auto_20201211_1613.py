# Generated by Django 3.1.4 on 2020-12-11 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0014_auto_20201209_0852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username_prefix',
            new_name='prefix',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='username_suffix',
            new_name='suffix',
        ),
        migrations.AddField(
            model_name='profile',
            name='json',
            field=models.JSONField(default=dict),
        ),
    ]