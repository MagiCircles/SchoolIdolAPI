# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20150123_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='os',
            field=models.CharField(default=b'iOs', max_length=10, choices=[(b'Android', b'Android'), (b'iOs', b'iOs')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='japanese_card_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='japanese_center_skill',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='japanese_center_skill_details',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='japanese_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='japanese_skill',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='japanese_skill_details',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='round_card_url',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='center',
            field=models.ForeignKey(blank=True, to='api.OwnedCard', help_text=b'The character that talks to you on your home screen.', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='friend_id',
            field=models.PositiveIntegerField(help_text=b'You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='language',
            field=models.CharField(default=b'JP', help_text=b'This is the version of the game you play.', max_length=10, choices=[(b'JP', b'Japanese'), (b'EN', b'English'), (b'KR', b'Korean'), (b'CH', b'Chinese')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='transfer_code',
            field=models.CharField(help_text=b"It's important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.", max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='card',
            field=models.ForeignKey(related_name='ownedcard', to='api.Card'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='stored',
            field=models.CharField(default=b'Deck', max_length=30, choices=[(b'Deck', b'In deck'), (b'Album', b'In album'), (b'Box', b'In present box'), (b'Favorite', b'Favorite Cards')]),
            preserve_default=True,
        ),
    ]
