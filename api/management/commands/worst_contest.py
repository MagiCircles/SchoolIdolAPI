from contest import models
from django.conf import settings
from web.templatetags.mod import tourldash
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        query = ''
        for contest in models.Contest.objects.filter(id__lte=settings.GLOBAL_CONTEST_ID):
            if contest.votes.count() < 10:
                continue
            try:
                if contest.image:
                    print '\n[![{}](http://i.schoolido.lu/{})\n\n{} {}](http://schoolido.lu/contest/{}/{}/)\n'.format(contest.name, contest.image, contest.name, ('(' + unicode(contest.begin.date()) + ' - ' + unicode(contest.end.date()) + ')' if contest.begin and contest.end else ''), contest.id, tourldash(contest.name))
                else:
                    print '\n[{} {}](http://schoolido.lu/contest/{}/{}/)\n'.format(contest.name, ('(' + unicode(contest.begin.date()) + ' - ' + unicode(contest.end.date()) + ')' if contest.begin and contest.end else ''), contest.id, tourldash(contest.name))
                _votes = models.Vote.objects.filter(contest=contest).order_by('counter').select_related('card')
                if contest.id == settings.GLOBAL_CONTEST_ID:
                    _votes = _votes.exclude(card__id__gt=569)
                _votes = _votes[:20]
                votes = []
                for vote in _votes:
                    # check if already in
                    if next((v for v in votes if v.card == vote.card), None) is None:
                        if (not (contest.name == 'Who\'s the best N?' and vote.card.id == 882)
                            and not (contest.name == 'What\'s your favorite Nozomi card?' and vote.card.id == 632)
                            and not (contest.name == 'What\'s your favorite event card?' and vote.card.id == 645)
                            and not (contest.name == 'What\'s your favorite Nico card?' and vote.card.id == 653)
                            and not (contest.name == 'Who\'s the cutest in a swimsuit?' and vote.card.id == 135)
                            and not (contest.name == 'Who\'s the cutest in a swimsuit?' and vote.card.id == 154)
                            and not (contest.name == 'Who\'s the most gorgeous mermaid?' and vote.card.id == 126)
                            and not (contest.name == 'What\'s your favorite Kotori card?' and vote.card.id == 677)
                            and not (contest.name == 'What\'s your favorite Eli card?' and vote.card.id == 712)
                            and not (contest.name == 'What\'s your favorite Eli card?' and vote.card.id == 711)
                        ):
                            votes.append(vote)
                votes = votes[:3]
                for (pos, vote) in enumerate(votes):
                    print '![{}](http://schoolido.lu/static/medal{}.png) [![{}](http://i.schoolido.lu/{})](http://schoolido.lu/cards/{}/)\n\n'.format(pos + 1, pos + 1, vote.card, (vote.card.round_card_idolized_image if vote.idolized or not vote.card.round_card_image else vote.card.round_card_image), vote.card.id)
                for w in votes:
                    v = str(w.card.id) + ('i' if w.idolized else 'n')
                    if v not in query:
                        query += v + ','
                print '***'
            except IndexError: pass
        print query[:-1]
        
