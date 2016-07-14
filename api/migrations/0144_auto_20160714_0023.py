# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0143_auto_20160713_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(related_name='notifications', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='url_data',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
