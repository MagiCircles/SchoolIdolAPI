# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20150406_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='verified',
            field=models.PositiveIntegerField(default=0, choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='beginning',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='otonokizaka',
            field=models.CharField(validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')], max_length=20, blank=True, help_text=b'Write your UID only, no URL.', null=True, verbose_name=b'Otonokizaka.org Forum'),
            preserve_default=True,
        ),
    ]
