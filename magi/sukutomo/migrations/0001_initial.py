# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators
import magi.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('nickname', models.CharField(max_length=20, verbose_name='Nickname')),
                ('rank', models.PositiveIntegerField(null=True, verbose_name='Rank')),
                ('i_version', models.PositiveIntegerField(default=1, verbose_name='Version', choices=[(0, 'Japanese'), (1, 'Worldwide'), (2, 'Korean'), (3, 'Chinese'), (4, 'Taiwanese')])),
                ('friend_id', models.PositiveIntegerField(help_text='You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.', null=True, verbose_name='Friend ID')),
                ('show_friend_id', models.BooleanField(default=True, verbose_name='Should your friend ID be visible to other players?')),
                ('accept_friend_requests', models.NullBooleanField(verbose_name='Accept friend requests')),
                ('device', models.CharField(help_text='The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...', max_length=150, null=True, verbose_name='Device')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date', validators=[django.core.validators.MinValueValidator(datetime.date(2013, 4, 16)), magi.utils.PastOnlyValidator])),
                ('show_start_date', models.BooleanField(default=True, help_text='Should this date be visible to other players?', verbose_name=b'')),
                ('loveca', models.PositiveIntegerField(default=0, help_text="Number of Love gems you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name='Love gems')),
                ('friend_points', models.PositiveIntegerField(default=0, help_text="Number of Friend Points you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name='Friend Points')),
                ('g', models.PositiveIntegerField(default=0, help_text="Number of G you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name=b'G')),
                ('tickets', models.PositiveIntegerField(default=0, help_text="Number of Scouting Tickets you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name=b'Scouting Tickets')),
                ('vouchers', models.PositiveIntegerField(default=0, help_text="Number of Vouchers (blue tickets) you currently have in your account. This field is completely optional, it's here to help you manage your accounts.", verbose_name=b'Vouchers (blue tickets)')),
                ('bought_loveca', models.PositiveIntegerField(help_text='You can calculate that number in "Other" then "Purchase History". Leave it empty to stay F2P.', null=True, verbose_name='Total love gems bought')),
                ('show_items', models.BooleanField(default=True, help_text='Should your items be visible to other players?', verbose_name=b'')),
                ('i_play_with', models.PositiveIntegerField(null=True, verbose_name='Play with', choices=[(0, b'Index'), (1, b'Hand'), (2, b'Other'), (3, b'Thumbs'), (4, b'Fingers')])),
                ('i_os', models.PositiveIntegerField(null=True, verbose_name='Operating System', choices=[(0, b'Android'), (1, b'iOs')])),
                ('transfer_code', models.CharField(help_text="It's important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.", max_length=100, verbose_name='Transfer Code')),
                ('fake', models.BooleanField(default=False, verbose_name='Fake')),
                ('owner', models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
