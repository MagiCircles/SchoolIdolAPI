# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_account_accept_friend_requests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreferences',
            name='accept_friend_requests',
        ),
    ]
