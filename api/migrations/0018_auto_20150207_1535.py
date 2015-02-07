# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20150204_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='language',
            field=models.CharField(default=b'JP', help_text=b'This is the version of the game you play.', max_length=10, choices=[(b'JP', b'Japanese'), (b'EN', b'English'), (b'KR', b'Korean'), (b'CN', b'Chinese'), (b'TW', b'Taiwanese')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_idolized_image',
            field=models.ImageField(null=True, upload_to=b'web/static/cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_image',
            field=models.ImageField(null=True, upload_to=b'web/static/cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='round_card_image',
            field=models.ImageField(null=True, upload_to=b'web/static/cards/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='stored',
            field=models.CharField(default=b'Deck', max_length=30, choices=[(b'Deck', b'In deck'), (b'Album', b'In album'), (b'Box', b'In present box'), (b'Favorite', b'Wish List')]),
            preserve_default=True,
        ),
    ]
