#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def importcards_japanese():
    print '### Import japanese information for R/SR/UR/promo'
    if local:
        fs = [open('jpcards.html', 'r')]
    else:
        fs = [urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/210.html'),
             urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/378.html'),
             urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/379.html'),
             urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/321.html'),
        ]
    for f in fs:
        soup = BeautifulSoup("".join(line.strip() for line in f.read().split("\n")))

        for tr in soup.find_all('tr'):
	            tds = tr.find_all('td')
	            if len(tds) > 4:
	                id = tds[0].string
	                try:
	                    id = int(id)
	                except (ValueError, TypeError):
	                    continue
	                if id != None:
	                    print 'Import for #', id, '...',; sys.stdout.flush()
	                    picture = tds[1].img
	                    if picture is not None:
	                        picture = wikiaImageURL(picture.get('src'))
	                    if tds[2].span is not None:
	                        tmp = tds[2].span.extract()
	                    if tds[2].br is not None:
	                        tmp = tds[2].br.extract()
	                    name = clean(tds[2].string)
	                    if name is not None and '(' in name:
	                        version = clean(name.split('(')[-1].split(')')[0])
	                        name = clean(name.split('(')[0])
	                    elif name is not None and '（' in name:
	                        version = clean(name.split('（')[-1].split('）')[0])
	                        name = clean(name.split('（')[0])
	                    else:
	                        version = ''
	                    if len(tds) == 5: # special cards ( no skill column )
	                        skill_name = None
	                        skill_details = clean(tds[-1].string)
	                        center_skill_name = None
	                        center_skill_details = None
	                    elif len(tds) == 7: # special cards ( with skill columns )
	                        skill_name, skill_details = extract_skill(tds[-2])
	                        center_skill_name = None
	                        center_skill_details = None
	                    elif len(tds) == 14: # promo cards
	                        skill_name, skill_details = extract_skill(tds[-2])
	                        center_skill_name, center_skill_details = extract_skill(tds[-1])
	                    elif len(tds) == 18: # all info specified
	                        skill_name, skill_details = extract_skill(tds[-2])
	                        center_skill_name, center_skill_details = extract_skill(tds[-1])
	                    elif len(tds) == 16: # take center skill from previous line
	                        skill_name, skill_details = extract_skill(tds[-1])
	                    # elif len(tds) == 15: # take skill + center skill from previous line
	                    defaults = {}
	                    if picture is not None:
	                        defaults['round_card_url'] = picture
	                    if version is not None:
	                        defaults['japanese_collection'] = version
	                    if skill_name is not None:
	                        defaults['japanese_skill'] = skill_name
	                    if skill_details is not None:
	                        defaults['japanese_skill_details'] = skill_details
	                    if center_skill_name is not None:
	                        defaults['japanese_center_skill'] = center_skill_name
	                    if center_skill_details is not None:
	                        defaults['japanese_center_skill_details'] = center_skill_details
	                    card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
	                    card.idol.japanese_name = name
	                    card.save()
	                    if picture and not noimages and (redownload or not card.round_card_image):
	                        print 'Download image...',; sys.stdout.flush()
	                        card.round_card_image.save(str(card.id) + 'round.jpg', downloadFile(picture))
	                    print 'Done'

        f.close()

    print '### Import japanese information for N (round image + name)'
    if local:
        f = open('jpcardsN.html', 'r')
    else:
        f = urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/101.html')
    soup = BeautifulSoup("".join(line.strip() for line in f.read().split("\n")))

    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 4:
            id = tds[0].string
            if id != None:
                print 'Import for #', id, '...',; sys.stdout.flush()
                picture = tds[1].img
                if picture is not None:
                    picture = wikiaImageURL(picture.get('src'))
                if tds[2].span is not None:
                    tmp = tds[2].span.extract()
                if tds[2].br is not None:
                    tmp = tds[2].br.extract()
                name = clean(tds[2].string)
                defaults = {
                    'japanese_name': name,
                }
                if picture is not None:
                    defaults['round_card_url'] = picture
                card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
                if picture and not noimages and (redownload or not card.round_card_image):
                    print 'Download image...',; sys.stdout.flush()
                    card.round_card_image.save(str(card.id) + 'round.jpg', downloadFile(picture))
                print 'Done'

    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args
        noimages = 'noimages' in args

        importcards_japanese()
        import_raw_db()
