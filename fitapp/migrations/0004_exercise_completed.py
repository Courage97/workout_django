# Generated by Django 5.1.2 on 2024-11-26 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0003_exercise_preset_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]
