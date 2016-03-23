# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0115_auto_20160323_0756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='skill_up_cards',
            new_name='_skill_up_cards',
        ),
    ]
