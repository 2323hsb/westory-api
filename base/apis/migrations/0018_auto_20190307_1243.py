# Generated by Django 2.1.4 on 2019-03-07 03:43

import apis.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0017_auto_20190307_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploadImage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadimage',
            name='image',
            field=models.ImageField(upload_to=apis.models.user_directory_path),
        ),
    ]