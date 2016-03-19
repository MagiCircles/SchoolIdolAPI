#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def importcards_japanese(opt):
    local = opt['local']
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
	                    elif len(tds) == 7: # special cards ( with skill columns )
	                        skill_name, skill_details = extract_skill(tds[-2])
	                    elif len(tds) == 14: # promo cards
	                        skill_name, skill_details = extract_skill(tds[-2])
	                    elif len(tds) == 18: # all info specified
	                        skill_name, skill_details = extract_skill(tds[-2])
	                    elif len(tds) == 16:
	                        skill_name, skill_details = extract_skill(tds[-1])
	                    # elif len(tds) == 15: # take skill from previous line
	                    defaults = {}
	                    if version is not None:
	                        defaults['japanese_collection'] = version
	                    if skill_name is not None:
	                        defaults['japanese_skill'] = skill_name
	                    if skill_details is not None:
	                        defaults['japanese_skill_details'] = skill_details
	                    card, created = models.Card.objects.update_or_create(id=id, defaults=defaults)
	                    card.idol.japanese_name = name
	                    card.save()
	                    print 'Done'

        f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        opt = opt_parse(args)

        importcards_japanese(opt)
        import_raw_db()
