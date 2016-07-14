# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from api import models
from web.utils import send_email

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        notifications = models.Notification.objects.filter(email_sent=False).select_related('owner', 'owner__preferences')
        for notification in notifications:
            preferences = notification.owner.preferences
            if preferences.is_notification_email_allowed(notification.message):
                send_email(
                    subject=(u'School Idol Tomodachi' + u'✨ ' + u' Notification: ' + notification.english_message),
                    template_name = 'notification',
                    to=[notification.owner.email, 'contact@schoolido.lu'],
                    context={
                        'notification': notification,
                        'user': notification.owner,
                    },
                )
                # todo ios push notifications
                print 'Email sent to {}: {}'.format(notification.owner.username, notification.localized_message)
            else:
                print '  No email for {}: {}'.format(notification.owner.username, notification.localized_message)
            notification.email_sent = True
            notification.save()
