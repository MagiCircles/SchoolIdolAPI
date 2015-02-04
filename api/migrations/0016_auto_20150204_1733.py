# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150204_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='japanese_card_name',
            new_name='japanese_collection',
        ),
    ]
