# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_remove_userpreferences_accept_friend_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='mal',
            field=models.CharField(validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')], max_length=20, blank=True, help_text='Write your username only, no URL.', null=True, verbose_name=b'MyAnimeList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='otonokizaka',
            field=models.CharField(validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')], max_length=20, blank=True, help_text='Write your username only, no URL.', null=True, verbose_name=b'Otonokizaka.org Forum'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='twitch',
            field=models.CharField(blank=True, max_length=20, null=True, help_text='Write your username only, no URL.', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
    ]
