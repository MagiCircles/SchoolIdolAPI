# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0132_auto_20160607_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='japanese_name',
            field=models.CharField(unique=True, max_length=100, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moderationreport',
            name='fake_activity',
            field=models.ForeignKey(related_name='moderationreport', on_delete=django.db.models.deletion.SET_NULL, to='api.Activity', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moderationreport',
            name='fake_user',
            field=models.ForeignKey(related_name='moderationreport', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
