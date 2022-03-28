# Generated by Django 3.2.10 on 2022-03-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crontab_monitor', '0003_auto_20200306_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertlog',
            name='executed_time_ymdhm',
            field=models.CharField(db_index=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='alertlog',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='cron_format',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='name',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='selectoption',
            name='swarm',
            field=models.CharField(db_index=True, max_length=64, verbose_name='Swarm Name'),
        ),
        migrations.AlterField(
            model_name='selectoption',
            name='value',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Value'),
        ),
    ]
