# Generated by Django 4.2.7 on 2023-12-27 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool_app', '0007_trip_slug_trippart_slug_tripregistration_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='trippart',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tripregistration',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]