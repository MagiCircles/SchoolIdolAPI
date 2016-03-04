# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0105_card_promo_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveIntegerField(default=1, choices=[(0, 'Rejected'), (1, 'Pending'), (2, 'In Progress'), (3, 'Accepted')])),
                ('comment', models.TextField(help_text='If your report is accepted, the account will be marked as fake and will never appear in leaderboards. Provide proofs below.', null=True, verbose_name='Comment', blank=True)),
                ('moderation_comment', models.TextField(null=True, verbose_name='Comment', blank=True)),
                ('fake_account', models.ForeignKey(related_name='moderationreport', to='api.Account')),
                ('fake_eventparticipation', models.ForeignKey(related_name='moderationreport', to='api.EventParticipation')),
                ('images', models.ManyToManyField(related_name='report', to='api.UserImage')),
                ('moderated_by', models.ForeignKey(related_name='moderation_done', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('reported_by', models.ForeignKey(related_name='reports_sent', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
