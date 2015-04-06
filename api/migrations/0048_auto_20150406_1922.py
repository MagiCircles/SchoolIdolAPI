# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20150406_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreferences',
            name='play_with',
        ),
        migrations.AddField(
            model_name='account',
            name='play_with',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Play with', choices=[(b'Thumbs', 'Thumbs'), (b'Fingers', 'All fingers'), (b'Hand', 'One hand'), (b'Other', 'Other')]),
            preserve_default=True,
        ),
    ]
