# Generated by Django 4.2.2 on 2023-07-03 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emapp', '0011_feedermodel_contact_stationmodel_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationmodel',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
