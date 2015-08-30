# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_auto_20150815_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlink',
            name='relevance',
            field=models.PositiveIntegerField(null=True, verbose_name='How often do you tweet/steam/post about Love Live?', choices=[(0, 'Never'), (1, 'Sometimes'), (2, 'Often'), (3, 'Every single day')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userlink',
            name='type',
            field=models.CharField(max_length=20, verbose_name='Platform', choices=[(b'twitter', b'Twitter'), (b'facebook', b'Facebook'), (b'reddit', b'Reddit'), (b'line', b'LINE Messenger'), (b'tumblr', b'Tumblr'), (b'otonokizaka', b'Otonokizaka.org Forum'), (b'twitch', b'Twitch'), (b'steam', b'Steam'), (b'osu', b'Osu!'), (b'mal', b'MyAnimeList'), (b'instagram', b'Instagram')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userlink',
            name='value',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=64, verbose_name='Username/ID', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
    ]
