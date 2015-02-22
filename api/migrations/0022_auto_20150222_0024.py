# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0021_card_video_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(related_name='accounts_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='card',
            field=models.ForeignKey(related_name='ownedcards', to='api.Card'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownedcard',
            name='owner_account',
            field=models.ForeignKey(related_name='ownedcards', to='api.Account'),
            preserve_default=True,
        ),
    ]
