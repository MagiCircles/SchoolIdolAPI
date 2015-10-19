#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_icons():
    print '### Import icons from EliAyase github'
    cards = models.Card.objects.all().order_by('-id')
    for card in cards:
        print 'Add icons #', card.id, '... '
        if (not card.is_promo and not card.is_special) and (not card.round_card_image or redownload):
            print '  Normal...'
            url = 'https://raw.githubusercontent.com/EliAyase/icon/master/' + str(card.id) + '_icon.png'
            card.round_card_image.save(
                unicode(card.id) + 'Round' + card.name.split(' ')[-1] + '.png',
                downloadShrunkedImage(url))
        if not card.round_card_idolized_image or redownload:
            print '  Idolized...'
            url = 'https://raw.githubusercontent.com/EliAyase/icon/master/' + str(card.id) + '_icona.png'
            card.round_card_idolized_image.save(
                unicode(card.id) + 'RoundIdolized' + card.name.split(' ')[-1] + '.png',
                downloadShrunkedImage(url))
        print ' Done.'

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        global local, redownload
        local = 'local' in args
        redownload = 'redownload' in args

        import_icons()
        import_raw_db()
