# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20150216_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='japanese_t1_points',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='japanese_t1_rank',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='japanese_t2_points',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='japanese_t2_rank',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='note',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='accept_friend_requests',
            field=models.BooleanField(default=True, verbose_name='Accept friend requests'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='best_girl',
            field=models.CharField(max_length=200, null=True, verbose_name='Best girl', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='color',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Color', choices=[(b'Smile', 'Smile'), (b'Pure', 'Pure'), (b'Cool', 'Cool'), (b'All', 'All')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='description',
            field=models.TextField(help_text='Write whatever you want. You can add formatting and links using Markdown.', null=True, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='location',
            field=models.CharField(help_text='The city you live in.', max_length=200, null=True, verbose_name='Location', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='private',
            field=models.BooleanField(default=False, help_text='If your profile is private, people will only see your center.', verbose_name='Private Profile'),
            preserve_default=True,
        ),
    ]
