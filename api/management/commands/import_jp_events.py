# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_jp_events(opt):
    local, redownload, noimages = opt['local'], opt['redownload'], opt['noimages']
    print '### Import events from decaf wiki'
    if local:
        f = open('events.html', 'r')
    else:
        f = urllib2.urlopen('http://decaf.kouhi.me/lovelive/index.php?title=List_of_Events&action=edit')

    for line in f.readlines():
        line = h.unescape(line)
        data = str(line).split('||')
        if len(data) > 1:
            name = clean(data[1].replace('[[', '').replace(']]', '').split('|')[-1]).replace('μs', 'μ\'s')
            dates = data[0].replace('|', '').split(' - ')
            beginning = eventDateFromString(clean(dates[0]) + ' 4pm', timezone=japantz)
            end = eventDateFromString(str(beginning.year) + '/' + clean(dates[1]) + (' 2pm' if name == 'Medley Festival Round 11' else ' 3pm'), timezone=japantz)
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
            print 'Import event ', name, '...',; sys.stdout.flush()
            defaults = {
                'beginning': beginning,
                'end': end,
                'japanese_t1_points': t1_points,
                'japanese_t1_rank': (None if not t1_points else t1_rank),
                'japanese_t2_points': t2_points,
                'japanese_t2_rank': t2_rank,
                'note': note,
            }
            event, created = models.Event.objects.update_or_create(japanese_name=name, defaults=defaults)
            models.Card.objects.filter(event=event).update(release_date=beginning)
            print 'Done'
            if not local and not noimages and (redownload or not event.image):
                print "  Import event image...",
                try:
                    url = 'http://decaf.kouhi.me/lovelive/index.php?title=' + urllib.quote(name.encode('utf-8'))
                    f_event = urllib2.urlopen(url)
                    
                    event_soup = BeautifulSoup(f_event.read())
                    content = event_soup.find('div', { 'id': 'mw-content-text'})
                    if content is not None:
                        image = content.find('img')
                        if image is not None:
                            image = 'http://decaf.kouhi.me/' + image.get('src')
                            event.image.save(name + '.jpg', downloadShrunkedImage(image))
                            print 'Done'
                    f_event.close()
                except TypeError:
                    print "No page found"
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        opt = opt_parse(args)
        import_jp_events(opt)
        import_raw_db()
