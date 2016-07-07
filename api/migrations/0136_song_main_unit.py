# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0135_auto_20160706_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='main_unit',
            field=models.CharField(default=b"\xce\xbc's", max_length=20),
            preserve_default=True,
        ),
    ]
