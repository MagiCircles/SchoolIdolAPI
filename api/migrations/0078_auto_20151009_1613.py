# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0077_userpreferences_allowed_verifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationrequest',
            name='allow_during_events',
            field=models.BooleanField(default=False, help_text="Check this only if you don't care about the current event. You'll get verified faster.", verbose_name='Allow us to verify your account during events'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='verification',
            field=models.PositiveIntegerField(default=1, help_text='What kind of verification would you like?', verbose_name='Verification', choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, 'Bronze Verified')]),
            preserve_default=True,
        ),
    ]
