from django.core.management.base import BaseCommand, CommandError
import api.models as am
import contest.models as ac
import sys
import json
from urlparse import parse_qs
import django.utils.dateparse as dateparse

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        file_handle = open('contests.json', 'r')
        contests = json.loads(file_handle.read())
        file_handle.close()

        for contest in contests:
            new_contest = ac.Contest(pk=contest['id'], name=contest['name'])
            new_contest.query = contest['params']
            new_contest.begin = dateparse.parse_date(contest['begin'])
            new_contest.end = dateparse.parse_date(contest['end'])
            results = contest['result'].split(' ')
            for result in results:
                if result == 'best_girl':
                    new_contest.best_girl = True
                if result == 'best_card':
                    new_contest.best_card = True
            new_contest.save()
        print("#Create the first contest")
        contest = ac.Contest()
        contest.name = 'Who\'s the best girl?'
        contest.begin = None
        contest.end = None
        contest.query = ''
        contest.best_girl = True
        contest.best_card = True
        contest.save()
