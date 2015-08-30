from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from api import models

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        preferences = models.UserPreferences.objects.all().select_related('user').order_by('id')
        for preference in preferences:
            print 'Import %s...' % preference.user.username,
            i = 0
            for link in models.LINK_DICT:
                if hasattr(preference, link) and getattr(preference, link):
                    models.UserLink.objects.get_or_create(owner=preference.user, type=link, value=getattr(preference, link))
                    i += 1
            print '%s links, Done.' % i
        
