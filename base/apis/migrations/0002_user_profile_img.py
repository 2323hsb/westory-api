# Generated by Django 2.1.2 on 2018-10-26 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_img',
            field=models.URLField(blank=True, verbose_name="google's profile image url"),
        ),
    ]