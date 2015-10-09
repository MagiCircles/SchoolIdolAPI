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
            content = soup.find('div', { 'id': 'mw-content-text'})
            if content is not None:
                content.find('div', { 'id', 'toc' }).extract()
                defaults = {}
                wikitable = None
                if idx <= 9:
                    wikitable = content.find('table', { 'class': 'wikitable' })
                ul_ = content.find('ul')
                ul = ul_.find_all('li')
                for li in ul:
                    if li.b is not None:
                        title = clean(clean(li.b.extract()).replace(':', ''))
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

                idol, created = models.Idol.objects.update_or_create(name=idol, defaults=defaults)

            f.close()
            print 'Done'

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args

        import_idols()
        import_raw_db()
