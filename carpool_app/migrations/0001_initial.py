# Generated by Django 4.2.7 on 2023-11-08 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=10)),
                ('num_passenger_seats', models.IntegerField()),
                ('license_plate', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sign_Ups',
            fields=[
                ('sign_up_id', models.AutoField(primary_key=True, serialize=False)),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.people')),
            ],
        ),
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('trip_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.cars')),
            ],
        ),
        migrations.CreateModel(
            name='Trip_Parts',
            fields=[
                ('trip_part_id', models.AutoField(primary_key=True, serialize=False)),
                ('departure_time', models.TimeField()),
                ('distance', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('fee', models.IntegerField()),
                ('starting_point', models.CharField(max_length=20)),
                ('ending_point', models.CharField(max_length=20)),
                ('trip_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.trips')),
            ],
        ),
        migrations.CreateModel(
            name='Trip_Part_Sign_Ups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_up_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.sign_ups')),
                ('trip_part_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.trip_parts')),
            ],
        ),
        migrations.AddField(
            model_name='sign_ups',
            name='trip_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.trips'),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
                ('content', models.CharField(max_length=100)),
                ('reviewee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewee_id', to='carpool_app.people')),
                ('reviewer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_id', to='carpool_app.people')),
                ('trip_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.trips')),
            ],
        ),
        migrations.AddField(
            model_name='cars',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool_app.people'),
        ),
    ]
