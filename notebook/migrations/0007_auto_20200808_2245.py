# Generated by Django 3.0.8 on 2020-08-08 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import notebook.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notebook', '0006_narrative_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='narrative',
            options={'ordering': ('created_at',)},
        ),
        migrations.CreateModel(
            name='SoundRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='voice-records', validators=[notebook.models.ext_validator])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='narrative',
            name='sound',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notebook.SoundRecord'),
        ),
    ]
