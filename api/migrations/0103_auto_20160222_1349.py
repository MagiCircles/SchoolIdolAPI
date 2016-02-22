# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0102_auto_20160222_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='friend_points',
            field=models.PositiveIntegerField(default=0, help_text="Number of Friend Points you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name='Friend Points'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='g',
            field=models.PositiveIntegerField(default=0, help_text="Number of G you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name=b'G'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='tickets',
            field=models.PositiveIntegerField(default=0, help_text="Number of Scouting Tickets you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name=b'Scouting Tickets'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='vouchers',
            field=models.PositiveIntegerField(default=0, help_text="Number of Vouchers (blue tickets) you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name=b'Vouchers (blue tickets)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='bought_loveca',
            field=models.PositiveIntegerField(help_text='You can calculate that number in "Other" then "Purchase History". Leave it empty to stay F2P.', null=True, verbose_name='Total love gems bought', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='loveca',
            field=models.PositiveIntegerField(default=0, help_text="Number of Love gems you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name='Love gems'),
            preserve_default=True,
        ),
    ]
