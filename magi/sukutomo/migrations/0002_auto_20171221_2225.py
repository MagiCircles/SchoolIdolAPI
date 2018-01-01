# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sukutomo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='account',
            name='show_start_date',
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_leaderboard',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_leaderboards_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_color',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_preferences_i_status',
            field=models.CharField(max_length=12, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_preferences_twitter',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_username',
            field=models.CharField(max_length=32, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='bought_loveca',
            field=models.PositiveIntegerField(help_text='You can calculate that number in "Other" then "Purchase History".', null=True, verbose_name='Total love gems bought'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='i_play_with',
            field=models.PositiveIntegerField(null=True, verbose_name='Play with', choices=[(0, 'Thumbs'), (1, 'All fingers'), (2, 'Index fingers'), (3, 'One hand'), (4, 'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start Date'),
            preserve_default=True,
        ),
    ]
