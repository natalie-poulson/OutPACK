# Generated by Django 2.0.5 on 2018-10-13 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0004_auto_20181013_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='bio',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='current_city',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
