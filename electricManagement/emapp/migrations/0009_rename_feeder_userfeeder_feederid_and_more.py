# Generated by Django 4.2.2 on 2023-06-20 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emapp', '0008_alter_schedulemodel_status_userfeeder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfeeder',
            old_name='feeder',
            new_name='feederId',
        ),
        migrations.RenameField(
            model_name='userfeeder',
            old_name='user',
            new_name='userId',
        ),
    ]