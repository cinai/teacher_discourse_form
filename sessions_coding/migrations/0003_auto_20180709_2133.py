# Generated by Django 2.0.7 on 2018-07-10 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions_coding', '0002_auto_20180709_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skills',
            field=models.CharField(max_length=40),
        ),
    ]
