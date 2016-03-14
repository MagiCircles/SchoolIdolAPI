# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='result_image',
            field=models.ImageField(null=True, upload_to=b'contest_results/', blank=True),
            preserve_default=True,
        ),
    ]
