# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150204_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='idolized_maximum_statistics_cool',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='idolized_maximum_statistics_pure',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='idolized_maximum_statistics_smile',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='minimum_statistics_cool',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='minimum_statistics_pure',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='minimum_statistics_smile',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='non_idolized_maximum_statistics_cool',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='non_idolized_maximum_statistics_pure',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='non_idolized_maximum_statistics_smile',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
