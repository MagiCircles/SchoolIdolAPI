# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_auto_20150830_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlink',
            name='type',
            field=models.CharField(max_length=20, verbose_name='Platform', choices=[(b'twitter', b'Twitter'), (b'facebook', b'Facebook'), (b'reddit', b'Reddit'), (b'line', b'LINE Messenger'), (b'tumblr', b'Tumblr'), (b'otonokizaka', b'Otonokizaka.org Forum'), (b'twitch', b'Twitch'), (b'steam', b'Steam'), (b'osu', b'Osu!'), (b'mal', b'MyAnimeList'), (b'instagram', b'Instagram'), (b'myfigurecollection', b'MyFigureCollection'), (b'hummingbird', b'Hummingbird'), (b'youtube', b'YouTube'), (b'deviantart', b'DeviantArt'), (b'pixiv', b'Pixiv')]),
            preserve_default=True,
        ),
    ]
