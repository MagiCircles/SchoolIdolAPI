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
        permission = args[1]
        preferences = models.UserPreferences.objects.get(user__username=args[0])
        if not preferences.has_permission(permission):
            raise CommandError('Doesn\'t have this permission {}. All permissions: {}'.format(permission, preferences.staff_permissions))
        permissions = preferences.staff_permissions
        permissions.remove(permission)
        if not permissions:
            preferences._staff_permissions = None
            preferences.user.is_staff = False
            preferences.user.save()
            print 'Staff status revoked'
        else:
            preferences._staff_permissions = ','.join(permissions)
        preferences.save()
        print 'Permission {} removed. All permissions: {}'.format(permission, preferences.staff_permissions)
