# Generated by Django 2.1.7 on 2019-03-09 03:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_account_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='accounts',
            field=models.ManyToManyField(to='core.Account'),
        ),
        migrations.AddField(
            model_name='widget',
            name='config',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
