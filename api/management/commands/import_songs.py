# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_songs(opt):
    local, redownload, noimages = opt['local'], opt['redownload'], opt['noimages']
    events = models.Event.objects.exclude(japanese_name__contains='Score Match').exclude(japanese_name__contains='Medley Festival').exclude(japanese_name__contains='Challenge Festival').exclude(japanese_name__contains='again').order_by('beginning')
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
                song['name'] = cleanwithquotes(tds[1].find('a').text).replace('♥', '♡').replace('！', '!')
                print 'Import {}...'.format(song['name']),
                song['attribute'] = attribute_jphexcolors[tds[1]['style'].replace(';', '').split(':')[-1]]
                try:
                    song['BPM'] = int(clean(tds[2].text).split('-')[-1].replace('bpm', '0'))
                except:
                    song['BPM'] = 0
                try:
                    time = clean(tds[3].text)
                    song['time'] = int(time[:-3]) * 60 + int(time[-2:])
                except:
                    song['time'] = None
                song['easy_difficulty'] = int(clean(tds[4].text))
                song['easy_notes'] = int(clean(tds[5].text))
                song['normal_difficulty'] = int(clean(tds[6].text))
                song['normal_notes'] = int(clean(tds[7].text))
                song['hard_difficulty'] = int(clean(tds[8].text))
                song['hard_notes'] = int(clean(tds[9].text))
                song['expert_difficulty'] = None if clean(tds[10].text) == '-' else int(clean(tds[10].text))
                song['expert_random_difficulty'] = None if clean(tds[11].text) == '-' else int(clean(tds[11].text))
                song['expert_notes'] = None if not clean(tds[12].text) or clean(tds[12].text) == '-' else int(clean(tds[12].text))
                song['event'] = None
                if event:
                    song['event'] = events[event_index]
                    event_index += 1
                song['rank'] = rank
                song, created = models.Song.objects.update_or_create(name=song['name'], defaults=song)
                print 'Done.'
                if not local and (redownload or not song.image or not song.romaji_name):
                    print "  Import song image and/or song name...",
                    url = 'http://decaf.kouhi.me/lovelive/index.php?title=' + urllib.quote(song.name.replace('Piano Mix', 'Piano mix').replace('ぶる~べりぃ', 'ぶる～べりぃ').encode('utf-8'))
                    try:
                        f_song = urllib2.urlopen(url)
                        song_soup = BeautifulSoup(f_song.read())
                        content = song_soup.find('div', { 'id': 'mw-content-text'})
                        if content is not None:
                            image = content.find('img')
                            if (not song.image or redownload) and image is not None and not noimages:
                                image = 'http://decaf.kouhi.me/' + image.get('src')
                                song.image.save(song.name + '.jpg', downloadShrunkedImage(image))
                            title_line = content.find_all('li')[0]
                            if clean(title_line.find('b').text) == 'Title (romaji/English):':
                                title_line.find('b').extract()
                                song.romaji_name = clean(title_line.text)
                                song.translated_name = clean(title_line.text)
                            else:
                                if clean(title_line.find('b').extract().text) == 'Title (romaji):':
                                    song.romaji_name = clean(title_line.text)
                                title_line = content.find_all('li')[1]
                                if clean(title_line.find('b').extract().text) == 'Title (English):':
                                    song.translated_name = clean(title_line.text)
                            print 'Done'
                            song.save()
                        f_song.close()
                    except urllib2.HTTPError:
                        print 'Decaf wiki page doesn\'t exist'
                if redownload or song.itunes_id is None:
                    song_name = song.name.replace('&', ' ')
                    print '  Import itunes song id...'
                    url = u'https://itunes.apple.com/search?country=JP&term=' + song_name + (' μ\'s' if song_name != 'Super LOVE=Super LIVE!' else '')
                    print '     ', url
                    response = urllib.urlopen(url.encode("UTF-8"))
                    data = json.loads(response.read())
                    if 'results' in data and len(data['results']) and 'trackId' in data['results'][0]:
                        if song_name == 'Paradise Live' or song_name == 'Love wing bell' or song_name == 'Happy maker!':
                            song.itunes_id = data['results'][1]['trackId']
                        elif song_name == '思い出以上になりたくて':
                            song.itunes_id = 0
                        else:
                            song.itunes_id = data['results'][0]['trackId']
                        print 'Done.'
                    else:
                        # Try with Aqours
                        url = u'https://itunes.apple.com/search?country=JP&term=' + song_name + ' Aqours'
                        print '     ', url
                        response = urllib.urlopen(url.encode("UTF-8"))
                        data = json.loads(response.read())
                        if 'results' in data and len(data['results']) and 'trackId' in data['results'][0]:
                            song.itunes_id = data['results'][0]['trackId']
                            print 'Done.'
                        else:
                            # Try with A-RISE
                            url = u'https://itunes.apple.com/search?country=JP&term=' + song_name + ' A-RISE'
                            print '     ', url
                            response = urllib.urlopen(url.encode("UTF-8"))
                            data = json.loads(response.read())
                            if 'results' in data and len(data['results']) and 'trackId' in data['results'][0]:
                                song.itunes_id = data['results'][0]['trackId']
                                print 'Done.'
                            else:
                                # Try with nothing
                                url = u'https://itunes.apple.com/search?country=JP&term=' + song_name
                                print '     ', url
                                response = urllib.urlopen(url.encode("UTF-8"))
                                data = json.loads(response.read())
                                if 'results' in data and len(data['results']) and 'trackId' in data['results'][0] and song_name != 'LONELIEST BABY' and song_name != '好きですが好きですか?' and song_name != 'Storm in Lover' and song_name != 'Anemone heart' and song_name != 'なわとび' and song_name != 'Beat in Angel':
                                    song.itunes_id = data['results'][0]['trackId']
                                    print 'Done \033[33mwithout singer.\033[0m'
                                else:
                                    song.itunes_id = 0
                                    print '\033[91mNone found.\033[0m'
                    song.save()
                songs.append(song)
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        opt = opt_parse(args)
        import_songs(opt)
        import_raw_db()
