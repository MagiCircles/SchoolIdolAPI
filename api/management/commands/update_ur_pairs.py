from django.core.management.base import BaseCommand, CommandError
from api import models
from api.management.commands.importbasics import *
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

	opt = opt_parse(args)
	local, redownload, noimages = opt['local'], opt['redownload'], opt['noimages']

	cards = models.Card.objects.filter(rarity='UR', is_promo=False, is_special=False)
	collections = []
	for card in cards:
	    if card.translated_collection not in collections:
		collections.append(card.translated_collection)
	for collection in collections:
	    if collection !=  'Initial':
		cards = models.Card.objects.filter(translated_collection=collection, rarity='UR').order_by('id')
		if len(cards) % 2 == 0:
		    i = 0
		    while i < len(cards):
			cards[i].ur_pair = cards[i+1]
			cards[i].save()
			cards[i+1].ur_pair = cards[i]
			cards[i+1].save()
			i += 2
	cards = models.Card.objects.filter(rarity='UR', is_promo=False, is_special=False)
	for card in cards:
	    print card.id, card.ur_pair_id

	print "# Get order of UR pairs from drive document"
	if local:
	    f = open('urpairs.csv', 'r')
	else:
	    f = urllib2.urlopen('https://docs.google.com/spreadsheets/d/1ICEX5vFe95WKMNYeDJ6MOuGBIKgdcV-DI87z0Xa9ivg/pub?gid=0&single=true&output=csv')
	reader = csv.reader(f)
	for line in reader:
	    try:
		models.Card.objects.filter(id=int(line[0])).update(ur_pair_reverse=bool(int(line[2])), ur_pair_idolized_reverse=bool(int(line[3])))
	    except ValueError:
		pass
	    try:
		card = models.Card.objects.get(id=line[0])
		if line[4] and not card.clean_ur:
		    card.clean_ur.save(str(card.id) + (card.name.split(' ')[-1]) + 'CleanUR.png', downloadShrunkedImage(line[4]))
		if line[5] and not card.clean_ur_idolized:
		    card.clean_ur_idolized.save(str(card.id) + (card.name.split(' ')[-1]) + 'CleanURIdolized.png', downloadShrunkedImage(line[5]))
	    except (ObjectDoesNotExist, ValueError):
		pass
