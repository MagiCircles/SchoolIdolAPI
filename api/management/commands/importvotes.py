from django.core.management.base import BaseCommand, CommandError
import api.models as am
import contest.models as ac
import sys
import json
from urlparse import parse_qs
from django.conf import settings
import django.utils.dateparse as dateparse

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        file_handle = open('votes.json', 'r')
        votes = json.loads(file_handle.read())
        file_handle.close()

        for vote in votes:
            print vote
            new_vote = ac.Vote()
            new_vote.idolized = vote['idolized']
            new_vote.counter = vote['counter']
            id_contest = vote['contest'] if vote['contest'] != 0 else settings.GLOBAL_CONTEST_ID
            new_vote.contest = ac.Contest.objects.get(pk=vote['contest'])
            new_vote.card = am.Card.objects.get(id=vote['card'])
            new_vote.save()
