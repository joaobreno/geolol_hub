# Generated by Django 5.0.1 on 2024-02-29 02:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riot_api_key', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AdminSetInstance',
            fields=[
                ('singleton_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='riot_admin.adminset')),
            ],
        ),
    ]
