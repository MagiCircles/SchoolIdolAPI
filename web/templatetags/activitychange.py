from django import template
register = template.Library()

def activitychange(activity):
    code = unicode(activity.message) + unicode(activity.account.pk)
    if (activity.message == 'Added a card'
        or activity.message == 'Idolized a card'
        or activity.message == 'Max Leveled a card'
        or activity.message == 'Max Bonded a card'):
        code += unicode(activity.ownedcard.stored)
    return code

register.filter('activitychange', activitychange)
