# Generated by Django 4.2.2 on 2023-07-03 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emapp', '0012_alter_stationmodel_createdby'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedermodel',
            name='feederType',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='stationmodel',
            name='capacity',
            field=models.CharField(default='', max_length=64),
        ),
    ]
