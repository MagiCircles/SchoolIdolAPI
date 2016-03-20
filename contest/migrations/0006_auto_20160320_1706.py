# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0005_vote_negative_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='homepage_image',
            field=models.ImageField(null=True, upload_to=b'contest/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='result_image_by',
            field=models.ForeignKey(related_name='designed_contest_result_banners', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
