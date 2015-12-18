#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_idols():
    idols = getGirls()
    if not local:
        print "### Import idols"
        for (idx, (idol, _)) in enumerate(idols):
            if not idol:
                continue
            idol, created = models.Idol.objects.get_or_create(name=idol)
            if idol.attribute and not redownload:
                continue
            print '  Import Idol', idol, '...',
            f = urllib2.urlopen('http://decaf.kouhi.me/lovelive/index.php?title=' + urllib.quote(idol.name))
            soup = BeautifulSoup(f.read())
            html = soup.find('div', { 'id': 'mw-content-text'})
            if html is not None:
                html.find('div', { 'id', 'toc' }).extract()
                defaults = {}
                wikitable = None
                if idx <= 9:
                    wikitable = html.find('table', { 'class': 'wikitable' })
                ul_ = html.find('ul')
                ul = ul_.find_all('li')
                for li in ul:
                    if li.b is not None:
                        title = clean(clean(li.b.extract().text).replace(':', ''))
                        content = clean(li.text)
                        if title is not None and content is not None and content != '?' and content != ' ?' and content != 'B? / W? / H?' and content != '' and content != '?cm':
                            if title == 'Age':
                                defaults['age'] = content
                            elif title == 'Birthday':
                                split = content.replace(')', '').split('(')
                                birthday = dateutil.parser.parse(clean(split[0]))
                                sign = clean(split[-1])
                                defaults['birthday'] = birthday
                                defaults['astrological_sign'] = sign
                            elif title == 'Japanese Name':
                                defaults['japanese_name'] = content
                            elif title == 'Blood Type':
                                defaults['blood'] = content
                            elif title == 'Height':
                                defaults['height'] = content.replace('cm', '')
                            elif title == 'Three Sizes':
                                defaults['measurements'] = content
                            elif title == 'Favorite Food' or title == 'Favorite Foods':
                                defaults['favorite_food'] = content
                            elif title == 'Least Favorite Food' or title == 'Least Favorite Foods':
                                defaults['least_favorite_food'] = content
                            elif title == 'Hobbies':
                                defaults['hobbies'] = content
                            elif title == 'Main Attribute':
                                defaults['attribute'] = content
                            elif title == 'Year':
                                defaults['year'] = content
                            elif title == 'CV':
                                defaults['cv'] = content
                                if li.a:
                                    defaults['cv_url'] = li.a.get('href')
                            else:
                                print '/!\\ Unknown content', title, content
                if wikitable is not None:
                    ps = wikitable.find_all('p')
                    if len(ps) >= 2:
                        if ps[0].br is not None:
                            ps[0].br.extract()
                        defaults['summary'] = clean(ps[0].text)
                        if ps[1].a is not None:
                            url = ps[1].a.get('href')
                            defaults['official_url'] = url

                if idx <= 9:
                    tables = html.find_all('table', { 'class': 'wikitable' })
                    for table in tables:
                        th = table.find('th', { 'colspan': '6' })
                        if th is not None:
                            text = th.find('span').text
                            if '(' in text and '#' in text:
                                name = text.split('(')[1].split(')')[0]
                                name = name.replace(' Ver.', '').strip()
                                id_card = int(text.split('#')[-1].replace(']', ''))
                                print 'Set collection', name, 'for #', str(id_card)
                                models.Card.objects.filter(pk=id_card).update(translated_collection=name)
                idol, created = models.Idol.objects.update_or_create(name=idol, defaults=defaults)

            f.close()
            print 'Done'

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        global local, redownload
        local = 'local' in args
        redownload = 'redownload' in args

        import_idols()
        import_raw_db()
