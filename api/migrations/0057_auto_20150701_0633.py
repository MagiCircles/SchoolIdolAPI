# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_auto_20150701_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='otonokizaka',
            field=models.CharField(validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')], max_length=20, blank=True, help_text=b'Write your UID only, no URL.', null=True, verbose_name=b'Otonokizaka.org Forum'),
            preserve_default=True,
        ),
    ]
