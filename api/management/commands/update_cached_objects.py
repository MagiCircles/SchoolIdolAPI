from django.core.management.base import BaseCommand, CommandError
from api.management.commands.update_cards_owners import update_cards_owners
from api.management.commands.update_cards_rankings import update_cards_rankings

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        update_cards_owners({})
        update_cards_rankings({})
        update_cards_join_cache({})
