# Generated by Django 4.2.2 on 2023-06-20 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emapp', '0006_schedulemodel_feederid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrolemodel',
            name='control_panel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='control_panel', to='emapp.crudmodel'),
        ),
    ]
