from django import template
from api import models

register = template.Library()

def verifiedToString(value):
    return models.verifiedToString(value)

def playWithToString(value):
    return models.playWithToString(value)

skillsIcons = {
    'Score Up': 'scoreup',
    'Healer': 'healer',
    'Perfect Lock': 'perfectlock',
    'Perfect Charm': 'scoreup',
    'Rhythmical Charm': 'scoreup',
    'Timer Yell': 'healer',
    'Timer Charm': 'scoreup',
    'Rhythmical Yell': 'healer',
    'Total Charm': 'scoreup',
    'Total Trick': 'perfectlock',
    'Perfect Yell': 'healer',
    'Total Yell': 'healer',
    'Timer Trick': 'perfectlock',
}

def skillToFlaticon(skill):
    if skill in skillsIcons:
        return skillsIcons[skill]
    return 'skill'

register.filter('verifiedToString', verifiedToString)
register.filter('playWithToString', playWithToString)
register.filter('activityMessageToString', models.activityMessageToString)
register.filter('userStatusToString', models.statusToString)
register.filter('userStatusToColor', models.statusToColor)
register.filter('userStatusToColorString', models.statusToColorString)
register.filter('linkTypeToString', models.linkTypeToString)
register.filter('skillToFlaticon', skillToFlaticon)
