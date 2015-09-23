# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_verificationrequest_verification_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='image',
            field=models.FileField(null=True, upload_to=b'user_images/', blank=True),
            preserve_default=True,
        ),
    ]
