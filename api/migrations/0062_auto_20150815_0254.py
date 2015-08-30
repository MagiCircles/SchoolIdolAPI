# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0061_auto_20150808_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, choices=[(b'twitter', b'Twitter'), (b'facebook', b'Facebook'), (b'reddit', b'Reddit'), (b'line', b'LINE Messenger'), (b'tumblr', b'Tumblr'), (b'otonokizaka', b'Otonokizaka.org Forum'), (b'twitch', b'Twitch'), (b'steam', b'Steam'), (b'osu', b'Osu!'), (b'mal', b'MyAnimeList'), (b'instagram', b'Instagram')])),
                ('value', models.CharField(help_text='Write your username only, no URL.', max_length=64, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')])),
                ('owner', models.ForeignKey(related_name='links', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='twitter',
            field=models.CharField(max_length=15, null=True, blank=True),
            preserve_default=True,
        ),
    ]
