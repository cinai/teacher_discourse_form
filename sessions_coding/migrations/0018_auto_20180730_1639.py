# Generated by Django 2.0.5 on 2018-07-30 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions_coding', '0017_auto_20180730_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom_session',
            name='content',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]