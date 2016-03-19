from django.core.management.base import BaseCommand, CommandError
from api import models
import urllib2, urllib
import json
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError('Takes a username and a permission')
        if args[1] not in models.STAFF_PERMISSIONS_DICT:
            raise CommandError('Second argument must be a valid permission: {}'.format(models.STAFF_PERMISSIONS_DICT.keys()))
        permission = args[1]
        preferences = models.UserPreferences.objects.get(user__username=args[0])
        if preferences.has_permission(permission):
            raise CommandError('Already has this permission {}'.format(permission))
        if not preferences.user.is_staff:
            preferences.user.is_staff = True
            preferences.user.save()
            print '{} is now staff'.format(preferences.user.username)
        permissions = preferences.staff_permissions
        permissions.append(permission)
        permissions.sort()
        preferences._staff_permissions = ','.join(permissions)
        preferences.save()
        print 'New permission added. All permissions: {}'.format(preferences.staff_permissions)
