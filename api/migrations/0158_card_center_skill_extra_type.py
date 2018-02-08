# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0157_auto_20170125_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='center_skill_extra_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'main_unit', 'Main Unit'), (b'sub_unit', 'Sub Unit'), (b'year', 'Year')]),
            preserve_default=True,
        ),
    ]
