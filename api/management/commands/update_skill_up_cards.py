from django.core.management.base import BaseCommand, CommandError
from api import models

def update_skill_up_cards(opt={}):
    print '## Update skill up cards'
    promo_skills = [s['skill'] for s in models.Card.objects.filter(is_promo=True).order_by('skill').values('skill').distinct()]
    skills = {}
    for skill in promo_skills:
        skills[skill] = ','.join([str(card['id']) + '-' + card['name'].split(' ')[-1] for card in models.Card.objects.filter(is_promo=False, skill=skill).values('id', 'name')])
    print skills
    promo_cards = models.Card.objects.filter(is_promo=True)
    for card in promo_cards:
        previous_skill_up_cards = card._skill_up_cards
        card._skill_up_cards = skills[card.skill]
        if previous_skill_up_cards != card._skill_up_cards:
            card.save()
            print '  #{} {}'.format(card, card._skill_up_cards)
    promo_cards = models.Card.objects.filter(is_promo=True)
    for card in promo_cards:
        previous_skill_up_cards = card._skill_up_cards
        card._skill_up_cards = skills[card.skill]
        if previous_skill_up_cards != card._skill_up_cards:
            card.save()
            print '  #{} {}'.format(card, card._skill_up_cards)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_skill_up_cards()
