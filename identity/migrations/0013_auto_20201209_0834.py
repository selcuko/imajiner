# Generated by Django 3.1.4 on 2020-12-09 05:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0012_profile_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedinuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loggedinuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]