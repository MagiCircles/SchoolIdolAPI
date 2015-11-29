# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_auto_20151125_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='account_link',
            field=models.CharField(default='/user/db0/#1', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='account_name',
            field=models.CharField(default='\u30c7\u30d3 JP', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='account_picture',
            field=models.CharField(default='http://www.gravatar.com/avatar/8e731f8661ed8a4549e5445ccffe388a?s=100&d=http%3A%2F%2Fschoolido.lu%2Favatar%2Ftwitter%2Fdbschoolidol', max_length=100),
            preserve_default=False,
        ),
    ]
