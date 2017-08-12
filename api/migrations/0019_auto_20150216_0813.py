# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0018_auto_20150207_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(blank=True, max_length=6, null=True, choices=[(b'Smile', 'Smile'), (b'Pure', 'Pure'), (b'Cool', 'Cool'), (b'All', 'All')])),
                ('description', models.TextField(null=True)),
                ('best_girl', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('twitter', models.CharField(max_length=20, null=True, blank=True)),
                ('accept_friend_requests', models.BooleanField(default=True)),
                ('private', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='account',
            name='center',
            field=models.ForeignKey(blank=True, to='api.OwnedCard', help_text='The character that talks to you on your home screen.', null=True, verbose_name='Center'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='friend_id',
            field=models.PositiveIntegerField(help_text='You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.', null=True, verbose_name='Friend ID', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='language',
            field=models.CharField(default=b'JP', help_text='This is the version of the game you play.', max_length=10, verbose_name='Language', choices=[(b'JP', 'Japanese'), (b'EN', 'English'), (b'KR', 'Korean'), (b'CN', 'Chinese'), (b'TW', 'Taiwanese')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='nickname',
            field=models.CharField(max_length=20, verbose_name='Nickname', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='os',
            field=models.CharField(default=b'iOs', max_length=10, verbose_name='Operating System', choices=[(b'Android', b'Android'), (b'iOs', b'iOs')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='rank',
            field=models.PositiveIntegerField(null=True, verbose_name='Rank', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='transfer_code',
            field=models.CharField(help_text="It's important to always have an active transfer code, since it will allow you to retrieve your account in case you lose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.", max_length=30, verbose_name='Transfer Code', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='expiration',
            field=models.DateTimeField(default=None, null=True, verbose_name='Expiration', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='idolized',
            field=models.BooleanField(default=False, verbose_name='Idolized'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='max_bond',
            field=models.BooleanField(default=False, verbose_name='Max Bond (Kizuna)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='max_level',
            field=models.BooleanField(default=False, verbose_name='Max Level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='stored',
            field=models.CharField(default=b'Deck', max_length=30, verbose_name='Stored', choices=[(b'Deck', 'In deck'), (b'Album', 'In album'), (b'Box', 'In present box'), (b'Favorite', 'Wish List')]),
            preserve_default=True,
        ),
    ]
