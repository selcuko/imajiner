# Generated by Django 3.1.2 on 2020-11-21 16:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0011_auto_20201121_1905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='narrativetranslation',
            options={'ordering': ('-published_at', '-created_at')},
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='body',
            field=models.TextField(null=True, verbose_name='Body'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='edited_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last edited at'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='html',
            field=models.TextField(null=True, verbose_name='HTML'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('tr', 'Türkçe'), ('fr', 'Français'), ('de', 'Deustch'), ('ru', 'русский')], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='lead',
            field=models.TextField(blank=True, null=True, verbose_name='Summary'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Publication date'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='sketch',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='slug',
            field=models.SlugField(max_length=100, null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='narrativetranslation',
            name='uuid',
            field=models.UUIDField(default='a3e60300-2c13-11eb-8d87-c417fefa24bd', unique=True, verbose_name='UUID'),
            preserve_default=False,
        ),
    ]
