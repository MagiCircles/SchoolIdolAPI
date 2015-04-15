# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20150411_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownedcard',
            name='skill',
            field=models.PositiveIntegerField(default=1, verbose_name='Skill (Level)', validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
