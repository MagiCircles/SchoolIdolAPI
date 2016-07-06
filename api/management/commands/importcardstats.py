# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *
from django.db import transaction

@transaction.atomic
def importcardstats(opt):
    local = opt['local']
    print '### Import card ids & stats from decaf wiki'
    if local:
        f = open('decaf.html', 'r')
    else:
        f = urllib2.urlopen('http://decaf.kouhi.me/lovelive/index.php?title=List_of_Cards&action=edit')

    currentType = types['Normals']
    special = specials['None']
    for line in f.readlines():
        line = h.unescape(line)
        data = str(line).split('||')
        if len(data) == 1:
            name = clean(data[0].translate(None, '='))
            if name in types.keys():
                currentType = types[name]
                special = specials['None']
                note = ""
                center = None
            if name in specials.keys():
                special = specials[name]
                note = ""
                center = None
        elif len(data) > 2:
            id = int(clean(data[0]))
            print 'Importing card #', id, '...',; sys.stdout.flush()
            name = cleanwithquotes(data[1].split('|')[1].split('#')[0])
            type = clean(data[2])

            hp = 0
            minStats = (0, 0, 0)
            intStats = (0, 0, 0)
            maxStats = (0, 0, 0)
            nextData = 7
            skill = None
            promo = None
            release_date = None
            event_en = ''
            event_jp = ''
            event = None

            if len(data) > 3:
                if special != 2:
                    hp = int(clean(data[3]))
                else:
                    note = clean(data[3].split('|')[-1])
            if len(data) > 6:
                minStats = (int(clean(data[4])), int(clean(data[5])), int(clean(data[6])))
            if currentType != 'N' and special == 0 and len(data) > 14: # intermediate stats
                intStats = (int(clean(data[8])), int(clean(data[9])), int(clean(data[10])))
                maxStats = (int(clean(data[12])), int(clean(data[13])), int(clean(data[14])))
                nextData = 15
            elif len(data) > 10:
                maxStats = (int(clean(data[8])), int(clean(data[9])), int(clean(data[10])))
                nextData = 11
            if len(data) > nextData:
                skill = clean(data[nextData].split('|')[-1])
            if len(data) > nextData + 1:
                center = clean(data[nextData + 1].split('|')[-1])

            soup = BeautifulSoup(data[1])
            soupsmall = soup.small
            if soupsmall is not None:
                soupspan = soupsmall.span
                if soupspan is not None:
                    if special == 1:
                        promo = soupspan.text.split('c/w ')[-1].replace('[[', '').replace('|', ' (').replace(']]', ') ')
                    else:
                        if 'Added on' in soupspan.text:
                            release_date_str = soupspan.text.split('Added on ')[1]
                            release_date_str = release_date_str.replace(' (Seal Shop)', '')
                            release_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(release_date_str, '%B %d, %Y')))
                        elif 'event prize' in soupspan.text:
                            event_name = soupspan.text.split(' event prize')[0].replace(']]', '').replace('[[', '')
                            event_jp = event_name.split('|')[0]
                            event_en = event_name.split('|')[-1]
                            event, created = models.Event.objects.update_or_create(japanese_name=event_jp, defaults={
                                'romaji_name': event_en,
                            })

            defaults = {
                'name': name,
                'rarity': currentType,
                'attribute': type,
                'is_promo': special == 1,
                'promo_item': promo,
                'is_special': special == 2,
                'hp': hp,
                'minimum_statistics_smile': minStats[0],
                'minimum_statistics_pure': minStats[1],
                'minimum_statistics_cool': minStats[2],
                'non_idolized_maximum_statistics_smile': intStats[0],
                'non_idolized_maximum_statistics_pure': intStats[1],
                'non_idolized_maximum_statistics_cool': intStats[2],
                'idolized_maximum_statistics_smile': maxStats[0],
                'idolized_maximum_statistics_pure': maxStats[1],
                'idolized_maximum_statistics_cool': maxStats[2],
                'skill': skill,
                'center_skill': center,
            }
            if note:
                defaults['skill_details'] = note
            if release_date is not None:
                defaults['release_date'] = release_date
            if event is not None:
                defaults['event'] = event
            idol, created = models.Idol.objects.get_or_create(name=name)
            defaults['idol'] = idol
            card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
            print 'Done'
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        opt = opt_parse(args)

        importcardstats(opt)
        import_raw_db()
