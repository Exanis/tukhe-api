# Generated by Django 2.1.7 on 2019-03-09 06:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190309_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='CachedRequestResult',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('provider', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('result', django.contrib.postgres.fields.jsonb.JSONField()),
                ('expire_date', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cache', to='core.Account')),
            ],
        ),
    ]