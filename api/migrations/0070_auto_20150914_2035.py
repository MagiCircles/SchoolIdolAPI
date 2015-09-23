# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_verificationrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'user_images/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='verificationrequest',
            name='comment',
            field=models.TextField(help_text='If you have anything to say to the person who is going to verify your account, feel free to write it here!', null=True, verbose_name='Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='verificationrequest',
            name='images',
            field=models.ManyToManyField(related_name='request', to='api.UserImage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='verified',
            field=models.PositiveIntegerField(default=0, choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, 'Bronze Verified')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='account',
            field=models.ForeignKey(related_name='verificationrequest', to='api.Account', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='verification',
            field=models.PositiveIntegerField(default=0, verbose_name='Verification', choices=[(0, b''), (1, 'Silver Verified'), (2, 'Gold Verified'), (3, 'Bronze Verified')]),
            preserve_default=True,
        ),
    ]
