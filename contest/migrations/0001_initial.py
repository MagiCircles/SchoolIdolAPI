# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_auto_20160105_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('begin', models.DateTimeField(null=True)),
                ('end', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=300)),
                ('best_girl', models.BooleanField(default=False)),
                ('best_card', models.BooleanField(default=False)),
                ('query', models.CharField(max_length=4092, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fingerprint', models.CharField(max_length=300)),
                ('token', models.CharField(max_length=36)),
                ('date', models.DateTimeField()),
                ('contest', models.ForeignKey(related_name='sessions', to='contest.Contest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idolized', models.BooleanField(default=False)),
                ('counter', models.PositiveIntegerField(default=0)),
                ('card', models.ForeignKey(related_name='votes', to='api.Card')),
                ('contest', models.ForeignKey(related_name='votes', to='contest.Contest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='session',
            name='left',
            field=models.ForeignKey(related_name='left', to='contest.Vote'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='right',
            field=models.ForeignKey(related_name='right', to='contest.Vote'),
            preserve_default=True,
        ),
    ]
