from django.core.management.base import BaseCommand
from api import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        hashtag = args[0]
        post = models.Activity.objects.filter(message_data__icontains=hashtag, account_id=1).order_by('id')[0]
        entries = models.Activity.objects.filter(id__gt=post.id, message_data__icontains=hashtag)
        print 'Total entries for {}:'.format(hashtag)
        print '{} participants'.format(entries.exclude(message_data__contains='JustForFun').count())
        print '{} just for fun'.format(entries.filter(message_data__contains='JustForFun').count())
