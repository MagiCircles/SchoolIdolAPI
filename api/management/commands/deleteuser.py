from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Specify username'
            return
        username = args[0]
        user = User.objects.get(username=username)
        user.delete()
        print '%s Deleted' % (user)
