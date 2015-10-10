# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_auto_20151009_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('romaji_name', models.CharField(max_length=100, null=True, blank=True)),
                ('translated_name', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute', models.CharField(max_length=6, choices=[(b'Smile', 'Smile'), (b'Pure', 'Pure'), (b'Cool', 'Cool'), (b'All', 'All')])),
                ('BPM', models.PositiveIntegerField(null=True, blank=True)),
                ('time', models.PositiveIntegerField(null=True, blank=True)),
                ('rank', models.PositiveIntegerField(null=True, blank=True)),
                ('daily_rotation', models.CharField(max_length=2, null=True, blank=True)),
                ('daily_rotation_position', models.PositiveIntegerField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'songs/', blank=True)),
                ('easy_difficulty', models.PositiveIntegerField(null=True, blank=True)),
                ('easy_notes', models.PositiveIntegerField(null=True, blank=True)),
                ('normal_difficulty', models.PositiveIntegerField(null=True, blank=True)),
                ('normal_notes', models.PositiveIntegerField(null=True, blank=True)),
                ('hard_difficulty', models.PositiveIntegerField(null=True, blank=True)),
                ('hard_notes', models.PositiveIntegerField(null=True, blank=True)),
                ('expert_difficulty', models.PositiveIntegerField(null=True, blank=True)),
                ('expert_random_difficulty', models.PositiveIntegerField(null=True, blank=True)),
                ('expert_notes', models.PositiveIntegerField(null=True, blank=True)),
                ('event', models.ForeignKey(related_name='songs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Event', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
