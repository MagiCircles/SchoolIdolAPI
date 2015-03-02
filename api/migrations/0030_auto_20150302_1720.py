# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_card_japanese_video_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='facebook',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='line',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='reddit',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='tumblr',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='twitter',
            field=models.CharField(help_text='Write your username only, no URL.', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
