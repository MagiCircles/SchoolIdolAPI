#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_transparent_images():
    print '### Import transparent images'
    if local:
        f = open('transparent.csv', 'r')
    else:
        f = urllib2.urlopen('https://docs.google.com/spreadsheets/d/1r8KuZjIRMz47LAOriTOAKDewIiKU8wkGdBJcfThHrC8/pub?gid=0&single=true&output=csv')
    reader = csv.reader(f)
    for line in reader:
        id = optInt(line[0])
        collection = optString(clean(line[2]))
        normal = optString(clean(line[3]))
        idolized = optString(clean(line[4]))
        ur_pair_normal = optString(clean(line[5]))
        ur_pair_idolized = optString(clean(line[6]))
        card = None
        if id is not None and collection:
            print 'Add english collection to #', id, '... ',
            card, created = models.Card.objects.update_or_create(id=id, defaults={
                'english_collection': collection,
            })
            print 'Done'
        if id is not None and (normal or idolized or ur_pair_normal or ur_pair_idolized):
            if not card:
                card = models.Card.objects.get(pk=id)
            print 'Add transparent images #', id, '... ',
            if normal and not card.transparent_image:
                card.transparent_image.save(str(card.id) + 'Transparent.png', downloadShrunkedImage(normal))
            if idolized and not card.transparent_idolized_image:
                card.transparent_idolized_image.save(str(card.id) + 'idolizedTransparent.png', downloadShrunkedImage(idolized))
            if ur_pair_normal and not card.transparent_ur_pair:
                card.transparent_ur_pair.save(str(card.id) + 'TransparentURpair.png', downloadShrunkedImage(ur_pair_normal))
            if ur_pair_idolized and not card.transparent_idolized_ur_pair:
                card.transparent_idolized_ur_pair.save(str(card.id) + 'idolizedTransparentURpair.png', downloadShrunkedImage(ur_pair_idolized))
            print 'Done'
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args

        import_transparent_images()
        import_raw_db()
