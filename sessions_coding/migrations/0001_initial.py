# Generated by Django 2.0.7 on 2018-07-10 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Axis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axis', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Classroom_session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wav_name', models.CharField(max_length=30)),
                ('duration', models.IntegerField(blank=True, default=0)),
                ('content', models.CharField(blank=True, max_length=30)),
                ('date', models.DateTimeField(blank=True)),
                ('path', models.FilePathField(path='C:\\Users\\usuario\\Documents\\Audios y textos\\clusters ciae\\data\\textos_ulloa')),
            ],
        ),
        migrations.CreateModel(
            name='Copus_code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('long_name', models.TextField()),
                ('eng_code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Learning_goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_name', models.CharField(max_length=30)),
                ('long_name', models.TextField()),
                ('axis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions_coding.Axis')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions_coding.Subject'),
        ),
        migrations.AddField(
            model_name='classroom_session',
            name='colegio',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='sessions_coding.School'),
        ),
        migrations.AddField(
            model_name='classroom_session',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions_coding.Grade'),
        ),
        migrations.AddField(
            model_name='classroom_session',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions_coding.Teacher'),
        ),
        migrations.AddField(
            model_name='axis',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions_coding.Subject'),
        ),
    ]
