# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_en_events():
    print '### Import EN events T1/T2 cutoffs from decaf wiki'
    if local:
        f = open('eventsEN.html', 'r')
    else:
        f = urllib2.urlopen('http://decaf.kouhi.me/lovelive/index.php?title=English_Version_Info&action=edit')

    cards_section = False
    for line in f.readlines():
        line = h.unescape(line)
        if line.startswith('=== '):
            if line.startswith('=== All Cards ==='):
                cards_section = True
            else:
                cards_section = False
        data = str(line).split('||')
        if cards_section and len(data) > 1:
            card_id = int(data[0].split('|')[-1].strip())
            print 'Set card #', card_id, ' as worldwide available...',
            models.Card.objects.filter(pk=card_id).update(japan_only=False)
            print 'Done'
        elif len(data) >= 5 and len(data) <= 8:
            dates = data[0].replace('|', '').split(' - ')
            beginning = eventDateFromString(dates[0])
            end = eventDateFromString(str(beginning.year) + '/' + dates[1])
            names = data[1].replace('[[', '').replace(']]', '').split('|')
            japanese_name = cleanwithquotes(names[-2])
            english_name = clean(names[-1])
            t1_points = optInt(clean(data[3]))
            i = 4
            if 'rowspan' in data[i] or len(data) == 7 or len(data) == 8:
                t1_new_rank = optInt(clean(data[i].split('|')[-1]))
                if t1_new_rank: t1_rank = t1_new_rank
                i = i + 1
            t2_points = optInt(data[i])
            i = i + 1
            if len(data) > i and ('rowspan' in data[i] or len(data) == 7 or len(data) == 8):
                t2_new_rank = optInt(clean(data[i].split('|')[-1]))
                if t2_new_rank: t2_rank = t2_new_rank
                i = i + 1
            note = None
            if len(data) > i:
                note = optString(clean(data[i].split('|')[-1]))
            print 'Import event ', english_name, '...',; sys.stdout.flush()
            defaults = {
                'english_name': english_name,
                'english_beginning': beginning,
                'english_end': end,
                'english_t1_points': t1_points,
                'english_t1_rank': (None if not t1_points else t1_rank),
                'english_t2_points': t2_points,
                'english_t2_rank': t2_rank,
            }
            event, created = models.Event.objects.update_or_create(japanese_name=japanese_name, defaults=defaults)

            print 'Done'
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args

        import_en_events()
        import_raw_db()
