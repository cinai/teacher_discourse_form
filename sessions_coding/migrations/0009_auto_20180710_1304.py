# Generated by Django 2.0.7 on 2018-07-10 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sessions_coding', '0008_auto_20180709_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='skills',
            new_name='skill',
        ),
    ]
