# Generated by Django 4.2.5 on 2024-01-21 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0002_rename_date_userprogress_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile/%Y/%m/%d/'),
        ),
    ]
