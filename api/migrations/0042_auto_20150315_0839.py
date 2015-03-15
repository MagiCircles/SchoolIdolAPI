# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20150310_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='center_skill',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='hp',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='japanese_center_skill',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='japanese_center_skill_details',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='japanese_skill',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='japanese_skill_details',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='skill_details',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='color',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Attribute', choices=[(b'Smile', 'Smile'), (b'Pure', 'Pure'), (b'Cool', 'Cool'), (b'All', 'All')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='description',
            field=models.TextField(help_text='Write whatever you want. You can add formatting and links using Markdown.', null=True, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='facebook',
            field=models.CharField(blank=True, max_length=20, null=True, help_text='Write your username only, no URL.', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='line',
            field=models.CharField(blank=True, max_length=20, null=True, help_text='Write your username only, no URL.', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='reddit',
            field=models.CharField(blank=True, max_length=20, null=True, help_text='Write your username only, no URL.', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='tumblr',
            field=models.CharField(blank=True, max_length=20, null=True, help_text='Write your username only, no URL.', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='twitter',
            field=models.CharField(blank=True, max_length=20, null=True, help_text='Write your username only, no URL.', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z-_\\.]*$', b'Only alphanumeric and - _ characters are allowed.')]),
            preserve_default=True,
        ),
    ]
