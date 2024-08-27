# Generated by Django 4.2.15 on 2024-08-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_remove_movie_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.CharField(max_length=255),
        ),
    ]
