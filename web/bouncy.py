from django.dispatch import receiver
from django_bouncy.models import Bounce
from django_bouncy.signals import feedback
from api import models

@receiver(feedback, sender=Bounce)
def process_feedback(sender, **kwargs):
    instance = kwargs['instance']
    if instance.hard:
        models.UserPreferences.objects.filter(user__email=instance.address).update(invalid_email=True)
