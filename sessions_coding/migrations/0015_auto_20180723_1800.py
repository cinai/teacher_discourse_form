# Generated by Django 2.0.5 on 2018-07-23 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions_coding', '0014_auto_20180720_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learning_goal',
            name='goal_name',
            field=models.TextField(),
        ),
    ]