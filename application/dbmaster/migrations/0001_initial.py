# Generated by Django 4.0 on 2022-04-12 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
            ],
            options={
                'verbose_name_plural': 'Public Holiday ',
            },
        ),
        migrations.CreateModel(
            name='SalaryYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='WorkingHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_hour_name', models.CharField(max_length=100)),
                ('normal_hour', models.CharField(max_length=2)),
                ('sun', models.CharField(max_length=2)),
                ('mon', models.CharField(max_length=2)),
                ('tue', models.CharField(max_length=2)),
                ('wed', models.CharField(max_length=2)),
                ('thu', models.CharField(max_length=2)),
                ('fri', models.CharField(max_length=2)),
                ('sat', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Working Hours',
            },
        ),
        migrations.CreateModel(
            name='SalaryPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.PositiveSmallIntegerField()),
                ('active', models.BooleanField(default=0)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbmaster.salaryyear')),
            ],
            options={
                'verbose_name_plural': 'Salary Dates',
            },
        ),
        migrations.CreateModel(
            name='HolidayDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_date', models.DateField()),
                ('holiday_name', models.CharField(max_length=100)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbmaster.holiday')),
            ],
            options={
                'verbose_name_plural': 'Holiday Dates',
            },
        ),
    ]
