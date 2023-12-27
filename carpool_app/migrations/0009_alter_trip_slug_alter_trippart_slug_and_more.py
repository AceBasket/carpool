# Generated by Django 4.2.7 on 2023-12-27 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool_app', '0008_alter_trip_slug_alter_trippart_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='trippart',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tripregistration',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
