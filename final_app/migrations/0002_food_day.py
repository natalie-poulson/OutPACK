# Generated by Django 2.0.5 on 2018-12-07 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='day',
            field=models.IntegerField(null=True),
        ),
    ]
