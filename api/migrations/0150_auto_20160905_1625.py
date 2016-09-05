# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0149_userpreferences_invalid_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='default_tab',
            field=models.CharField(default=b'following', help_text='The activities you see by default on the homepage.', max_length=30, verbose_name='Default tab', choices=[(b'following', 'Following'), (b'all', 'All'), (b'hot', 'Hot')]),
            preserve_default=True,
        ),
    ]
