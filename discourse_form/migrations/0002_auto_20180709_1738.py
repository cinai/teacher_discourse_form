# Generated by Django 2.0.7 on 2018-07-09 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discourse_form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answered_subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discourse_form.Form_answer')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='answered_subject',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discourse_form.Subject'),
        ),
    ]