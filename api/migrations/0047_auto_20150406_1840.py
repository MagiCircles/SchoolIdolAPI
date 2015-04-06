# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_account_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='device',
            field=models.CharField(help_text='The modele of your device. Example: Nexus 5, iPhone 4, iPad 2, ...', max_length=150, null=True, verbose_name='Device', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='play_with',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Play with', choices=[(b'Thumbs', 'Thumbs'), (b'Fingers', 'All fingers'), (b'Hand', 'One hand'), (b'Other', 'Other')]),
            preserve_default=True,
        ),
    ]
