# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_userpreferences_location_changed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('birthday', models.DateField(default=None, null=True, blank=True)),
                ('blood', models.CharField(max_length=3, null=True, blank=True)),
                ('height', models.PositiveIntegerField(null=True, blank=True)),
                ('measurements', models.CharField(max_length=20, null=True, blank=True)),
                ('favorite_food', models.CharField(max_length=100, null=True, blank=True)),
                ('least_favorite_food', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute', models.CharField(max_length=6, choices=[(b'Smile', 'Smile'), (b'Pure', 'Pure'), (b'Cool', 'Cool'), (b'All', 'All')])),
                ('cv', models.CharField(unique=True, max_length=100)),
                ('summary', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
