# Generated by Django 5.0.1 on 2024-03-01 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riot_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminset',
            name='status_key',
            field=models.BooleanField(default=False),
        ),
    ]
