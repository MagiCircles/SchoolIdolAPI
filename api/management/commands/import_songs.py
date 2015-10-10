# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_songs():
    events = models.Event.objects.exclude(japanese_name__contains='Score Match').exclude(japanese_name__contains='Medley Festival').exclude(japanese_name__contains='again').order_by('beginning')
    print '### Import songs'
    if local:
        f = open('songs.html', 'r')
    else:
        f = urllib2.urlopen('http://www59.atwiki.jp/lovelive-sif/pages/115.html')

    soup = BeautifulSoup(f.read())
    content = soup.find('div', { 'id': 'wikibody'})
    songs = []
    section = 0
    event_index = 0
    if content is not None:
        table = content.find_all('table')[1]
        rank = 0
        for tr in table.find('tbody').find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) == 1:
                if section != 0:
                    rank = None
                event = section == 1
                daily_rotation = section == 4
                available = section != 2
                section += 1
            if len(tds) == 13 or len(tds) == 12:
                song = { 'available': available }
                if len(tds) == 12:
                    tds.insert(0, '')
                else:
                    if clean(tds[0]['style']).split(':')[1].split(';')[0] == 'lightblue':
                        song['available'] = False
                    else:
                        try: rank = int(tds[0].text)
                        except ValueError:
                            if daily_rotation:
                                song['daily_rotation'], song['daily_rotation_position'] = clean(tds[0].text).split('-')
                song['name'] = cleanwithquotes(tds[1].find('a').text).replace('♥', '♡')
                print 'Import {}...'.format(song['name']),
                song['attribute'] = attribute_jphexcolors[tds[1]['style'].replace(';', '').split(':')[-1]]
                song['BPM'] = int(clean(tds[2].text).split('-')[-1])
                time = clean(tds[3].text)
                song['time'] = int(time[:-3]) * 60 + int(time[-2:])
                song['easy_difficulty'] = int(clean(tds[4].text))
                song['easy_notes'] = int(clean(tds[5].text))
                song['normal_difficulty'] = int(clean(tds[6].text))
                song['normal_notes'] = int(clean(tds[7].text))
                song['hard_difficulty'] = int(clean(tds[8].text))
                song['hard_notes'] = int(clean(tds[9].text))
                song['expert_difficulty'] = None if clean(tds[10].text) == '-' else int(clean(tds[10].text))
                song['expert_random_difficulty'] = None if clean(tds[11].text) == '-' else int(clean(tds[11].text))
                song['expert_notes'] = None if clean(tds[12].text) == '-' else int(clean(tds[12].text))
                song['event'] = None
                if event:
                    song['event'] = events[event_index]
                    event_index += 1
                song['rank'] = rank
                song, created = models.Song.objects.update_or_create(name=song['name'], defaults=song)
                print 'Done.'
                if not local and not noimages and (redownload or not song.image):
                    print "  Import song image...",
                    url = 'http://decaf.kouhi.me/lovelive/index.php?title=' + urllib.quote(song.name.replace('Piano Mix', 'Piano mix').replace('ぶる~べりぃ', 'ぶる～べりぃ').encode('utf-8'))
                    f_song = urllib2.urlopen(url)
                    song_soup = BeautifulSoup(f_song.read())
                    content = song_soup.find('div', { 'id': 'mw-content-text'})
                    if content is not None:
                        image = content.find('img')
                        if image is not None:
                            image = 'http://decaf.kouhi.me/' + image.get('src')
                            song.image.save(song.name + '.jpg', downloadShrunkedImage(image))
                        title_line = content.find_all('li')[0]
                        if clean(title_line.find('b').extract().text) == 'Title (romaji):':
                            song.romaji_name = clean(title_line.text)
                        title_line = content.find_all('li')[1]
                        if clean(title_line.find('b').extract().text) == 'Title (English):':
                            song.translated_name = clean(title_line.text)
                        print 'Done'
                        song.save()
                    f_song.close()
                songs.append(song)
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        global local, redownload, noimages
        local = 'local' in args
        redownload = 'redownload' in args
        noimages = 'noimages' in args

        import_songs()
        import_raw_db()
