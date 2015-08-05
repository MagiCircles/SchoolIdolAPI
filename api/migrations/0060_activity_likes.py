# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0059_auto_20150706_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='likes',
            field=models.ManyToManyField(related_name='liked_activities', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
