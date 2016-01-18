# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_auto_20151222_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='default_tab',
            field=models.CharField(default=b'deck', help_text='What people see first when they take a look at your account.', max_length=30, verbose_name='Default tab', choices=[(b'deck', 'Deck'), (b'album', 'Album'), (b'teams', 'Teams'), (b'events', 'Events'), (b'wishlist', 'Wish List'), (b'presentbox', 'Present Box'), (b'activities', 'Activities')]),
            preserve_default=True,
        ),
    ]
