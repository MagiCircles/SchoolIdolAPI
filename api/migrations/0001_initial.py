# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(default=b'', max_length=20)),
                ('friend_id', models.PositiveIntegerField(default=0)),
                ('transfer_code', models.CharField(default=b'', max_length=30)),
                ('language', models.CharField(default=b'JP', max_length=10, choices=[(b'JP', b'Japanese'), (b'EN', b'English'), (b'KR', b'Korean'), (b'CH', b'Chinese')])),
                ('rank', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.PositiveIntegerField(help_text=b'Number of the card in the album', unique=True, serialize=False, primary_key=3)),
                ('name', models.CharField(max_length=100)),
                ('rarity', models.CharField(max_length=10, choices=[(b'N', b'Normal'), (b'R', b'Rare'), (b'SR', b'Super Rare'), (b'UR', b'Ultra Rare')])),
                ('attribute', models.CharField(max_length=6, choices=[(b'Smile', b'Smile'), (b'Pure', b'Pure'), (b'Cool', b'Cool'), (b'All', b'All')])),
                ('is_promo', models.BooleanField(default=False, help_text=b'Promo cards are already idolized. It is not possible to scout them, since they come with bought items or in the game on special occasions.')),
                ('is_special', models.BooleanField(default=False, help_text=b'Special cards cannot be added in a team but they can be used in training.')),
                ('hp', models.PositiveIntegerField()),
                ('minimum_statistics_smile', models.PositiveIntegerField()),
                ('minimum_statistics_pure', models.PositiveIntegerField()),
                ('minimum_statistics_cool', models.PositiveIntegerField()),
                ('non_idolized_maximum_statistics_smile', models.PositiveIntegerField()),
                ('non_idolized_maximum_statistics_pure', models.PositiveIntegerField()),
                ('non_idolized_maximum_statistics_cool', models.PositiveIntegerField()),
                ('idolized_maximum_statistics_smile', models.PositiveIntegerField()),
                ('idolized_maximum_statistics_pure', models.PositiveIntegerField()),
                ('idolized_maximum_statistics_cool', models.PositiveIntegerField()),
                ('skill', models.TextField()),
                ('skill_details', models.TextField()),
                ('center_skill', models.TextField()),
                ('card_url', models.CharField(max_length=200)),
                ('card_idolized_url', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='account',
            name='center',
            field=models.ForeignKey(to='api.Card'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(related_name='account', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
