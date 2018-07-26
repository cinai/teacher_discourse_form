# Generated by Django 2.0.5 on 2018-07-26 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discourse_form', '0009_answered_axis_phrases'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answered_skill_phrases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrases', models.TextField()),
                ('ans_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discourse_form.Form_answer')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discourse_form.Answered_skill')),
            ],
        ),
    ]
