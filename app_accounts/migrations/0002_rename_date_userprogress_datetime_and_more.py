# Generated by Django 4.2.5 on 2023-11-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprogress',
            old_name='date',
            new_name='datetime',
        ),
        migrations.AlterField(
            model_name='userstatistic',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
