# Generated by Django 4.2.2 on 2023-07-06 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emapp', '0013_feedermodel_feedertype_stationmodel_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrolemodel',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group', to='emapp.crudmodel'),
        ),
        migrations.CreateModel(
            name='GroupModel',
            fields=[
                ('seq_num', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name', 'createdBy'],
            },
        ),
        migrations.CreateModel(
            name='GroupFeeder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feederId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emapp.feedermodel')),
                ('groupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emapp.groupmodel')),
            ],
        ),
    ]