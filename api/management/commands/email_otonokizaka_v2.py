# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _, string_concat
from api import models
from web.utils import send_email
from django.db.models import Prefetch
import sys
import csv

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        users = models.User.objects.filter(links__type='otonokizaka').prefetch_related(Prefetch('links', queryset=models.UserLink.objects.filter(type='otonokizaka'), to_attr='otonokizaka_links')).distinct()
        for user in users:
            print 'Sending email to ', user.email
            for l in user.otonokizaka_links:
                print ' ', l.value, l.type
            send_email(subject=(string_concat(_(u'School Idol Tomodachi'), u'✨ ', ' Otonokizaka.org Forum version 2 is up! Re-create your account now~')),
                       template_name='otonokizakav2',
                       to=[user.email],
                       context={
                           'user': user,
                       },
            )
            models.UserLink.objects.filter(pk__in=[l.id for l in user.otonokizaka_links]).delete()
            print '  deleted'
