# Generated by Django 3.1.4 on 2020-12-09 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0015_narrativetranslation_edited'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='narrative',
            options={'ordering': ('author',)},
        ),
        migrations.RemoveField(
            model_name='narrative',
            name='edited_at',
        ),
        migrations.RemoveField(
            model_name='narrative',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='narrative',
            name='published_at',
        ),
    ]
