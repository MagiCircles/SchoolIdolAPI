from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from api import models
from contest import models as cmodels

adjusted_today = date.today()

# 1-13 - OR - 16-28 - OR - 24-5 - OR - 8-20

def get_long_dates(birthday):
    birthday = birthday.replace(year=adjusted_today.year)
    year = 2017 if birthday >= adjusted_today else 2018
    if birthday.day >= 1 and birthday.day <= 13:
        return (date(year=year, month=birthday.month, day=1),
                date(year=year, month=birthday.month, day=13))
    elif birthday.day >= 16 and birthday.day <= 28:
        return (date(year=year, month=birthday.month, day=16),
                date(year=year, month=birthday.month, day=28))
    elif birthday.day >= 8 and birthday.day <= 20:
        return (date(year=year, month=birthday.month, day=8),
                date(year=year, month=birthday.month, day=20))
    elif birthday.day >= 24:
        return (date(year=year, month=birthday.month, day=24),
                date(year=year, month=birthday.month + 1, day=5))

# 1-5 - 6-11 - 12-18 - 19-24 - 25-30

def get_short_dates(birthday):
    birthday = birthday.replace(year=adjusted_today.year)
    year = 2017 if birthday >= adjusted_today else 2018
    if birthday.day >= 1 and birthday.day <= 5:
        return (date(year=year, month=birthday.month, day=1),
                date(year=year, month=birthday.month, day=5))
    elif birthday.day >= 6 and birthday.day <= 11:
        return (date(year=year, month=birthday.month, day=6),
                date(year=year, month=birthday.month, day=11))
    elif birthday.day >= 12 and birthday.day <= 18:
        return (date(year=year, month=birthday.month, day=12),
                date(year=year, month=birthday.month, day=18))
    elif birthday.day >= 19 and birthday.day <= 24:
        return (date(year=year, month=birthday.month, day=19),
                date(year=year, month=birthday.month, day=24))
    elif birthday.day >= 25:
        return (date(year=year, month=birthday.month, day=25),
                date(year=year, month=birthday.month, day=30))

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        for idol in models.Idol.objects.filter(birthday__isnull=False).order_by('birthday'):
            begin, end = get_long_dates(idol.birthday) if idol.main else get_short_dates(idol.birthday)
            name = u'What\'s your favorite {} card? {}'.format(
                idol.name.split(' ')[-1],
                ('2017 ed.' if idol.birthday.month > 3 else ('2nd ed' if idol.main and idol.main_unit == 'Aqours' else '3rd ed.')) if idol.main else '')
            print u'{}\t{}\t{}'.format(name, begin, end)
            try:
                cmodels.Contest.objects.get(name=name)
            except ObjectDoesNotExist:
                cmodels.Contest.objects.create(name=name, begin=begin, end=end, best_card=True, best_girl=False, query='?idol__name={}'.format(idol.name))
