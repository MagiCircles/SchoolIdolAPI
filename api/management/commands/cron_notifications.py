# -*- coding: utf-8 -*-
import time
from django.core.management.base import BaseCommand, CommandError
from api import models
from web.utils import send_email

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        sent = []
        notifications = models.Notification.objects.filter(email_sent=False).select_related('owner', 'owner__preferences')
        for notification in notifications:
            preferences = notification.owner.preferences
            if preferences.is_notification_email_allowed(notification.message):
                notification_sent = notification.owner.email + notification.english_message + notification.website_url
                print time.strftime("%Y-%m-%d %H:%M"),
                if notification_sent in sent:
                    print u' Duplicate not sent to {}: {}'.format(notification.owner.username, notification.english_message)
                elif notification.message == models.NOTIFICATION_LIKE:
                    print u' TMP disable likes NOT sent to {}: {}'.format(notification.owner.username, notification.english_message)
                else:
                    sent.append(notification_sent)
                    try:
                        send_email(
                            subject=(u'School Idol Tomodachi' + u'✨ ' + u' Notification: ' + notification.english_message),
                            template_name = 'notification',
                            to=[notification.owner.email],
                            context={
                                'notification': notification,
                                'user': notification.owner,
                            },
                        )
                        print u'Email sent to {}: {}'.format(notification.owner.username, notification.english_message)
                    except Exception, e:
                        print u'!! Error when sending email to {} !!'.format(notification.owner.email)
                        print e
                        notification.owner.preferences.invalid_email = True
                        notification.owner.preferences.save()
            else:
                print '  No email for {}: {}'.format(notification.owner.username, notification.localized_message)
            notification.email_sent = True
            notification.save()
