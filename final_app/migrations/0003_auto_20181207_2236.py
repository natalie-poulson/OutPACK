# Generated by Django 2.0.5 on 2018-12-07 22:36

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0002_food_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326),
        ),
    ]
