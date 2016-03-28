# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0117_auto_20160324_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsicalVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry', models.PositiveIntegerField(default=0, choices=[(1, b'<iframe style="width: 100%" height="200" src="http://www.youtube.com/embed/AvacR2G0Q9w?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'), (2, b'<iframe style="width: 100%" height="200" src="http://www.youtube.com/embed/AvacR2G0Q9w?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'), (3, b'<iframe style="width: 100%" height="200" src="http://www.youtube.com/embed/AvacR2G0Q9w?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'), (4, b'<iframe style="width: 100%" height="200" src="http://www.youtube.com/embed/AvacR2G0Q9w?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'), (5, b'<iframe style="width: 100%" height="200" src="http://www.youtube.com/embed/AvacR2G0Q9w?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'), (6, b'<iframe style="width: 100%" height="200" src="http://www.youtube.com/embed/AvacR2G0Q9w?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>')])),
                ('user', models.ForeignKey(related_name='usical_vote', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
