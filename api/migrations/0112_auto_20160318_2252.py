# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0111_auto_20160312_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreferences',
            old_name='allowed_verifications',
            new_name='_staff_permissions',
        ),
    ]
