# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *
from api.management.commands.importcardstats import importcards_stats
from api.management.commands.import_jp_events import import_jp_events
from api.management.commands.import_en_events import import_en_events
from api.management.commands.import_wikia import import_wikia
from api.management.commands.importcards_japanese import importcards_japanese
from api.management.commands.import_transparent_images import import_transparent_images
from api.management.commands.import_video_stories import import_video_stories
from api.management.commands.import_idols import import_idols

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        local = 'local' in args
        redownload = 'redownload' in args
        noimages = 'noimages' in args

        if 'delete' in args:
            models.Card.objects.all().delete()
            models.Event.objects.all().delete()
            models.Idol.objects.all().delete()
            return

        importcards_stats()
        import_jp_events()
        import_en_events()
        import_wikia()
        importcards_japanese()
        if not noimages:
            import_transparent_images()
        import_video_stories()
        import_idols()

        import_raw_db()
