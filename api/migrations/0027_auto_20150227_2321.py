# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_event_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ranking', models.PositiveIntegerField(null=True, verbose_name='Ranking', blank=True)),
                ('song_ranking', models.PositiveIntegerField(null=True, verbose_name='Song Ranking', blank=True)),
                ('points', models.PositiveIntegerField(null=True, verbose_name='Points', blank=True)),
                ('account', models.ForeignKey(related_name='events', to='api.Account')),
                ('event', models.ForeignKey(related_name='participations', to='api.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventparticipation',
            unique_together=set([('event', 'account')]),
        ),
        migrations.AlterField(
            model_name='card',
            name='event',
            field=models.ForeignKey(related_name='cards', blank=True, to='api.Event', null=True),
            preserve_default=True,
        ),
    ]
