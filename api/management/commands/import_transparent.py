#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_transparent_images():
    print '### Import transparent images from EliAyase github'
    cards = models.Card.objects.all().order_by('-id')
    for card in cards:
        print 'Add transparent images #', card.id, '... '
        if (not card.is_promo and not card.is_special) and (not card.transparent_image or redownload):
            print '  Normal...'
            url = 'https://raw.githubusercontent.com/EliAyase/navi/master/' + str(card.id) + '.png'
            card.transparent_image.save(str(card.id) + 'Transparent.png', downloadShrunkedImage(url))
        if not card.transparent_idolized_image or redownload:
            print '  Idolized...'
            url = 'https://raw.githubusercontent.com/EliAyase/navi/master/' + str(card.id) + 'a.png'
            card.transparent_idolized_image.save(str(card.id) + 'idolizedTransparent.png', downloadShrunkedImage(url))
        print ' Done.'
        
class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        global local, redownload
        local = 'local' in args
        redownload = 'redownload' in args

        import_transparent_images()
        import_raw_db()
