# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0130_account_ranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderationreport',
            name='fake_activity',
            field=models.ForeignKey(related_name='moderationreport', to='api.Activity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='moderationreport',
            name='fake_user',
            field=models.ForeignKey(related_name='moderationreport', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
