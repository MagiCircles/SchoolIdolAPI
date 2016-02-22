# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0101_auto_20160221_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bought_loveca',
            field=models.PositiveIntegerField(help_text='You can calculate that number in "Other" then "Purchase History".', null=True, verbose_name='Total love gems bought', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='loveca',
            field=models.PositiveIntegerField(default=0, help_text="Number of love gems you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name='Love gems'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='message',
            field=models.CharField(max_length=300, choices=[(b'Added a card', 'Added {} in {}'), (b'Idolized a card', 'Idolized {} in {}'), (b'Rank Up', 'Rank Up {}'), (b'Ranked in event', 'Ranked {} in event {}'), (b'Verified', 'Just got verified: {}'), (b'Trivia', '{}/10 on School Idol Trivia! {}'), (b'Custom', b'Custom')]),
            preserve_default=True,
        ),
    ]
