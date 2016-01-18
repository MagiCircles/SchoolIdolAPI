# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0093_account_default_tab'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
                ('ownedcard', models.ForeignKey(to='api.OwnedCard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('owner_account', models.ForeignKey(related_name='teams', verbose_name='Account', to='api.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(related_name='members', to='api.Team'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('team', 'ownedcard'), ('team', 'position')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='default_tab',
            field=models.CharField(default=b'deck', help_text='What people see first when they take a look at your account.', max_length=30, verbose_name='Default tab', choices=[(b'deck', 'Deck'), (b'album', 'Album'), (b'teams', 'Teams'), (b'events', 'Events'), (b'wishlist', 'Wish List'), (b'presentbox', 'Present Box')]),
            preserve_default=True,
        ),
    ]
