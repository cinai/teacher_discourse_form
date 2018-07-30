# Generated by Django 2.0.5 on 2018-07-24 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discourse_form', '0008_form_answer_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answered_axis_phrases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrases', models.TextField()),
                ('ans_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discourse_form.Form_answer')),
                ('axis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discourse_form.Answered_axis')),
            ],
        ),
    ]