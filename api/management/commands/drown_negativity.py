from django.core.management.base import BaseCommand, CommandError
from api import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Q, F

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        models.Activity.objects.filter(Q(message_data__icontains='eunice') | Q(message_data__icontains='astin') | Q(message_data__icontains='suici')).update(creation=(timezone.now() - relativedelta(days=2)))
