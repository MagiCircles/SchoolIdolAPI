# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0142_privatemessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.PositiveIntegerField(choices=[(0, b'You have a new private message from {}.'), (1, b'{} liked your activity.'), (2, b'You have a new follower: {}.')])),
                ('message_data', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='has_unread_notifications',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
