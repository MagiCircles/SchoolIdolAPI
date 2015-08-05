from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Specify email address'
            return
        email = args[0]
        users = User.objects.filter(email=email)
        print email, ':',
        for user in users:
            print user.username,
        print ''
