# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0068_auto_20150914_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('verification_date', models.DateTimeField(auto_now_add=True)),
                ('verification', models.PositiveIntegerField(default=0, choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, b'')])),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, b'Pending'), (1, b'In Progress'), (2, b'Verified')])),
                ('account', models.ForeignKey(related_name='verificationrequests', to='api.Account')),
                ('verified_by', models.ForeignKey(related_name='verificationsdone', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
