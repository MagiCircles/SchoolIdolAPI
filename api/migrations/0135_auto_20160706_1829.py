# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0134_auto_20160623_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='rarity',
            field=models.CharField(max_length=10, choices=[(b'N', 'Normal'), (b'R', 'Rare'), (b'SR', 'Super Rare'), (b'SSR', 'Super Super Rare'), (b'UR', 'Ultra Rare')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='allow_during_events',
            field=models.BooleanField(default=False, help_text="Check this only if you accept to get verified anytime during any event. You'll get verified faster. If you don't care for most events but you plan to play seriously some events, feel free to specify a list of exceptions in the comment box above.", verbose_name='Allow us to verify your account during events'),
            preserve_default=True,
        ),
    ]
