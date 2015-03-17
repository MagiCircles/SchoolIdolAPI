from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
# from django.core.files.images import ImageFile
# from django.core.files.temp import NamedTemporaryFile
# from django.db.models import Count
# from django.forms.models import model_to_dict
# import urllib2, urllib
# from bs4 import BeautifulSoup, Comment
# from api import models
# import re
# import HTMLParser
# import unicodedata
# import sys
# import datetime
# import time
# import csv
# import json

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Specify email address'
            return
        email = args[0]
        users = User.objects.filter(email=email)
        print email, ':',
        for user in users:
            print user.username,
        print ''
