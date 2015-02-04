# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_auto_20150122_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=20, blank=True)),
                ('friend_id', models.PositiveIntegerField(blank=True)),
                ('transfer_code', models.CharField(max_length=30, blank=True)),
                ('language', models.CharField(default=b'JP', max_length=10, editable=False, choices=[(b'JP', b'Japanese'), (b'EN', b'English'), (b'KR', b'Korean'), (b'CH', b'Chinese')])),
                ('rank', models.PositiveIntegerField(blank=True)),
                ('center', models.ForeignKey(to='api.Card')),
                ('owner', models.ForeignKey(related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OwnedCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idolized', models.BooleanField(default=False)),
                ('stored', models.CharField(default=b'Deck', max_length=30, choices=[(b'Deck', b'In deck'), (b'Album', b'In album'), (b'Box', b'In present box')])),
                ('expiration', models.DateTimeField(default=None, null=True, blank=True)),
                ('card', models.ForeignKey(related_name='ownedcard', editable=False, to='api.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
