from django.core.management.base import BaseCommand, CommandError
from api import models
import urllib2, urllib
import json
import sys

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        staff = models.UserPreferences.objects.filter(_staff_permissions__isnull=False).exclude(_staff_permissions='').select_related('user')
        for u in staff:
            if '1' in u.staff_permissions or '2' in u.staff_permissions or '3' in u.staff_permissions:
                permissions = []
                for verification in u.staff_permissions:
                    permissions.append('VERIFICATION_' + verification)
                permissions = ','.join(permissions)
                print u.user.username, permissions
                u._staff_permissions = permissions
                u.save()

