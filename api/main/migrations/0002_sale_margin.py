# Generated by Django 4.2 on 2023-04-15 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='margin',
            field=models.FloatField(default=0),
        ),
    ]
