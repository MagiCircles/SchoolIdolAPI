# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150121_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('japanese_name', models.CharField(max_length=100)),
                ('english_name', models.CharField(max_length=100)),
                ('beginning', models.DateField(blank=True)),
                ('end', models.DateField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='account',
            name='center',
        ),
        migrations.RemoveField(
            model_name='account',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.AddField(
            model_name='card',
            name='event',
            field=models.ForeignKey(related_name='card', blank=True, to='api.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='promo_item',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='release_date',
            field=models.DateField(default=datetime.date(2013, 4, 16)),
            preserve_default=True,
        ),
    ]
