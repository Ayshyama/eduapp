# Generated by Django 4.2.5 on 2024-01-22 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_exercises', '0002_exercise_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='name',
            new_name='description',
        ),
    ]