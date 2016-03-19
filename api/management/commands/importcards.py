# -*- coding: utf-8 -*-
from api.management.commands.importbasics import *
from api.management.commands.importcardstats import importcardstats
from api.management.commands.import_jp_events import import_jp_events
from api.management.commands.import_en_events import import_en_events
from api.management.commands.import_wikia import import_wikia
from api.management.commands.importcards_japanese import importcards_japanese
from api.management.commands.import_transparent_images import import_transparent_images
from api.management.commands.import_video_stories import import_video_stories
from api.management.commands.import_idols import import_idols
from api.management.commands.import_songs import import_songs

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        opt = opt_parse(args)
        if opt['delete']:
            models.Card.objects.all().delete()
            models.Event.objects.all().delete()
            models.Idol.objects.all().delete()
            models.Song.objects.all().delete()
            return

        importcardstats(opt)
        import_jp_events(opt)
        import_en_events(opt)
        import_idols(opt)
        import_songs(opt)

        import_raw_db()
