from django.core.management.base import BaseCommand, CommandError
from web.templatetags.choicesToString import skillsIcons
from api import models

def update_skill_up_cards(opt={}):
    print '## Update skill up cards'
    all_skills = [skill for skill in skillsIcons.keys() if skill != 'Score Up' and skill != 'Healer' and skill != 'Perfect Lock']
    skills = {}
    for skill in all_skills:
        skills[skill] = ','.join([str(card['id']) + '-' + card['name'].split(' ')[-1] for card in models.Card.objects.filter(is_promo=False, skill=skill).exclude(idol__main_unit='A-RISE').exclude(idol__main_unit='Aqours').values('id', 'name')])
    print skills
    promo_cards = models.Card.objects.filter(skill__in=all_skills)
    for card in promo_cards:
        previous_skill_up_cards = card._skill_up_cards
        card._skill_up_cards = skills[card.skill].replace(str(card.id) + '-' + card.name.split(' ')[-1], '').replace(',,',',')
        if card._skill_up_cards[-1] == ',':
            card._skill_up_cards = card._skill_up_cards[:-1]
        if card._skill_up_cards[0] == ',':
            card._skill_up_cards = card._skill_up_cards[1:]
        if previous_skill_up_cards != card._skill_up_cards:
            card.save()
            print '  #{} {}'.format(card, card._skill_up_cards)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        update_skill_up_cards()
