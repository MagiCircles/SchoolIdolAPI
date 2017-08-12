# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_auto_20150830_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transfer_code',
            field=models.CharField(help_text="It's important to always have an active transfer code, since it will allow you to retrieve your account in case you lose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.", max_length=100, verbose_name='Transfer Code', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userlink',
            name='relevance',
            field=models.PositiveIntegerField(null=True, verbose_name='How often do you tweet/stream/post about Love Live?', choices=[(0, 'Never'), (1, 'Sometimes'), (2, 'Often'), (3, 'Every single day')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userlink',
            name='type',
            field=models.CharField(max_length=20, verbose_name='Platform', choices=[(b'twitter', b'Twitter'), (b'facebook', b'Facebook'), (b'reddit', b'Reddit'), (b'line', b'LINE Messenger'), (b'tumblr', b'Tumblr'), (b'otonokizaka', b'Otonokizaka.org Forum'), (b'twitch', b'Twitch'), (b'steam', b'Steam'), (b'osu', b'Osu!'), (b'mal', b'MyAnimeList'), (b'instagram', b'Instagram'), (b'myfigurecollection', b'MyFigureCollection'), (b'hummingbird', b'Hummingbird'), (b'youtube', b'YouTube'), (b'deviantart', b'DeviantArt'), (b'pixiv', b'Pixiv'), (b'github', b'GitHub')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userlink',
            name='value',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=64, verbose_name='Username/ID', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\. ]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='location',
            field=models.CharField(help_text='The city you live in.It might take up to 24 hours to update your location on the map.', max_length=200, null=True, verbose_name='Location', blank=True),
            preserve_default=True,
        ),
    ]
