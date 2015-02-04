# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150122_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='center_skill',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='promo_item',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill_details',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
