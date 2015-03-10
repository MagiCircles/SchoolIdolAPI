from django.core.management.base import BaseCommand, CommandError
from api import models
from geopy.geocoders import Nominatim
import time, sys

def getLatLong(geolocator, user):
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
            print user.user, user.location, 'Invalid location'
    except:
        print user.user, user.location, 'Error, ', sys.exc_info()[0], 'retry...'
        getLatLong(geolocator, user)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        reload = 'reload' in args

        map = models.UserPreferences.objects.filter(location__isnull=False).exclude(location__exact='')
        if not reload:
            map = map.filter(location_changed__exact=True)
        geolocator = Nominatim()
        for user in map:
            getLatLong(geolocator, user)
