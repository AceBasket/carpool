# Generated by Django 4.2.7 on 2023-11-11 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpool_app', '0003_rename_car_id_car_id_rename_review_id_review_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car', to=settings.AUTH_USER_MODEL),
        ),
    ]
