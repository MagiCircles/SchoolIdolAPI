#-*- coding: utf-8 -*-
from api.management.commands.importbasics import *

def import_video_stories(opt):
    print '### Import video stories'
    if local:
        f = open('videos.csv', 'r')
    else:
        f = urllib2.urlopen('https://docs.google.com/spreadsheets/d/1AlLTBEuxEBXSVcxE6PpyE8ZcjWfvAQQCsgnKQyFQlPY/export?gid=0&format=csv')
    reader = csv.reader(f)
    for line in reader:
        id = optInt(line[1])
        video = optString(clean(line[2]))
        japanese_video = optString(clean(line[3]))
        if id is not None and (video is not None or japanese_video is not None):
            print 'Add video story to #', id, '... ',
            card, created = models.Card.objects.update_or_create(id=id, defaults={
                'video_story': video,
                'japanese_video_story': japanese_video,
            })
            print 'Done'
    f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        opt = opt_parse(args)

        import_video_stories(opt)
        import_raw_db()
