# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0139_auto_20160707_0439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='round_card_idolized_image',
            new_name='english_round_card_idolized_image',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='round_card_image',
            new_name='english_round_card_image',
        ),
    ]
