from django.core.management.base import BaseCommand, CommandError
from api import models
from web.views import getUserAvatar, getUserPreferencesAvatar
from web.templatetags.imageurl import chibiimage
from geopy.geocoders import Nominatim
import time, sys
from django.utils.html import escape

def getLatLong(geolocator, user, retry):
    time.sleep(1)
    try:
        location = geolocator.geocode(user.location)
        if location is not None:
            user.latitude = location.latitude
            user.longitude = location.longitude
            user.location_changed = False
            user.save()
            print user.user, user.location, user.latitude, user.longitude
        else:
            user.location_changed = False
            user.save()
            print user.user, user.location, 'Invalid location'
    except:
        if retry:
            print user.user, user.location, 'Error, ', sys.exc_info()[0], 'retry...'
            getLatLong(geolocator, user)
        else:
            print user.user, user.location, 'Error, ', sys.exc_info()[0]

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        reload = 'reload' in args
        retry = 'retry' in args

        map = models.UserPreferences.objects.filter(location__isnull=False).exclude(location__exact='')
        if not reload:
            map = map.filter(location_changed__exact=True)
        geolocator = Nominatim()
        for user in map:
            getLatLong(geolocator, user, retry)

        map = models.UserPreferences.objects.filter(latitude__isnull=False).select_related('user')

        mapcount = map.count()
        f = open('mapcount.json', 'w')
        print >> f, mapcount
        f.close()

        mapcache = ""
        for u in map:
            mapcache += "  {'username': '%s',\
  'avatar': '%s',\
  'location': '%s',\
  'icon': '%s',\
  'latlong': new google.maps.LatLng(%f, %f) },\
" % (escape(u.user.username), escape(getUserPreferencesAvatar(u.user, u, 200)), escape(u.location), escape(chibiimage(u.best_girl)), u.latitude, u.longitude)
        with open('map.json', 'w') as f:
            f.write(mapcache.encode('UTF-8'))
        f.close()
