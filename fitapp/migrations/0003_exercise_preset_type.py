# Generated by Django 5.1.2 on 2024-11-24 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0002_alter_exercise_exercise_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='preset_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]