# Generated by Django 3.1.2 on 2020-11-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0003_profile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='shadow_priviledges',
            field=models.BooleanField(default=False),
        ),
    ]