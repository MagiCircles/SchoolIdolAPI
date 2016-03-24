# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_auto_20160323_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='_skill_up_cards',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
    ]
