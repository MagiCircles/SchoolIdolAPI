#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_wikia():
    print '### Import card pictures and skills details from wikia'
    if local:
        f = open('wikia.html', 'r')
    else:
        f = urllib2.urlopen('http://love-live.wikia.com/wiki/Love_Live!_School_Idol_Festival_Card_List')
    soup = BeautifulSoup(f.read())

    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 4:
            id = ""
            normal = ''
            idolized = ''
            skill = None
            id = tds[0].string
            if id is not None:
                id = int(clean(str(id)))
                print 'Import images & skill for #', id, '...',; sys.stdout.flush()
            normaltd = tds[1].a
            if normaltd is not None:
                normal = wikiaImageURL(normaltd.get('href'))
            idolizedtd = tds[2].a
            if idolizedtd is not None:
                idolized = wikiaImageURL(idolizedtd.get('href'))
            if tds[3].b is not None:
                skill_title = clean(tds[3].b.extract())
            if tds[3].br is not None:
                tds[3].br.extract()
            if tds[3].text is not None:
                skill = clean(tds[3].text)
            if id is not None:
                defaults = {
                    'card_url': normal,
                    'card_idolized_url': idolized,
                }
                if skill:
                    defaults['skill_details'] = skill
                card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
                if normal and not noimages and (redownload or not card.card_image):
                    card.card_image.save(str(card.id) + '.jpg', downloadBestWikiaImage(normal))
                if idolized and not noimages and (redownload or not card.card_idolized_image):
                    card.card_idolized_image.save(str(card.id) + 'idolized.jpg', downloadBestWikiaImage(idolized))
                print 'Done'
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args
        noimages = 'noimages' in args

        import_wikia()
        import_raw_db()
