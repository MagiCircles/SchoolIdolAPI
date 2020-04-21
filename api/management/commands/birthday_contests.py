import pytz, datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from api import models
from api.management.commands.giveaway_cheater import get_next_birthday
from contest import models as cmodels

# 1-13 - OR - 16-28 - OR - 24-5 - OR - 8-20

def get_long_dates(birthday):
    if birthday.day >= 1 and birthday.day <= 13:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=1, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=13, tzinfo=pytz.UTC))
    elif birthday.day >= 16 and birthday.day <= 28:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=16, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=28, tzinfo=pytz.UTC))
    elif birthday.day >= 8 and birthday.day <= 20:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=8, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=20, tzinfo=pytz.UTC))
    elif birthday.day >= 24:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=24, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month + 1, day=5, tzinfo=pytz.UTC))

# 1-5 - 6-11 - 12-18 - 19-24 - 25-30

def get_short_dates(birthday):
    if birthday.day >= 1 and birthday.day <= 5:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=1, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=5, tzinfo=pytz.UTC))
    elif birthday.day >= 6 and birthday.day <= 11:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=6, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=11, tzinfo=pytz.UTC))
    elif birthday.day >= 12 and birthday.day <= 18:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=12, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=18, tzinfo=pytz.UTC))
    elif birthday.day >= 19 and birthday.day <= 24:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=19, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=24, tzinfo=pytz.UTC))
    elif birthday.day >= 25:
        return (datetime.datetime(year=birthday.year, month=birthday.month, day=25, tzinfo=pytz.UTC),
                datetime.datetime(year=birthday.year, month=birthday.month, day=30, tzinfo=pytz.UTC))

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        # Fix birthdays if needed
        for idol in models.Idol.objects.filter(birthday__isnull=False).order_by('birthday'):
            idol.birthday = idol.birthday.replace(year=2015)
            idol.save()

        # Add contests

        already_exist = []
        not_enough_cards = []

        for idol in models.Idol.objects.filter(birthday__isnull=False).order_by('birthday'):

            next_birthday = get_next_birthday(idol.birthday)

            name = u'What\'s your favorite {idol_name} card? {year} ed.'.format(
                idol_name=idol.name.split(' ')[-1] if idol.name != 'Emma Verde' else 'Emma',
                year=next_birthday.year,
            )

            # Check for existing contest to avoid adding duplicates
            try:
                existing_contest = cmodels.Contest.objects.get(name=name)
                already_exist.append(existing_contest)
                continue
            except ObjectDoesNotExist:
                pass

            # Get dates
            begin, end = get_long_dates(next_birthday) if idol.main else get_short_dates(next_birthday)

            # Check that the idol has at least two cards
            if models.Card.objects.filter(idol=idol).count() < 2:
                not_enough_cards.append(idol)
                continue

            contest = cmodels.Contest.objects.create(
                name=name,
                begin=begin,
                end=end,
                best_card=True,
                best_girl=False,
                query='?idol__name={}'.format(idol.name),
            )

            print u'{}\t{}\t{}'.format(contest.name, contest.begin, contest.end)

        if already_exist:
            print ''
            print 'The following contest have not been added because they are already in database:'
            for contest in already_exist:
                print u'{}\t{}\t{}'.format(contest.name, contest.begin, contest.end)

        if not_enough_cards:
            print ''
            print 'The following contest have not been added because the idol doesn\'t have enough cards:'
            for idol in not_enough_cards:
                print idol.name

    print ''
