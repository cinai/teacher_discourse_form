# Generated by Django 2.0.7 on 2018-07-10 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse_form', '0003_form_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form_answer',
            name='ans_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date answered'),
        ),
    ]
