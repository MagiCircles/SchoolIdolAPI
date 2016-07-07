from django import template
from api import models
from django.utils.translation import ugettext_lazy as _, string_concat

register = template.Library()

def verifiedToString(value):
    return models.verifiedToString(value)

def playWithToString(value):
    return models.playWithToString(value)

def languageToString(value):
    return _(models.languageToString(value))

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

difficultyStrings = {
    'easy': _('Easy'),
    'normal': _('Normal'),
    'hard': _('Hard'),
    'expert': _('Expert'),
    'expert_random': _('Random'),
    'master': _('Master'),
}

def difficultyToString(difficulty):
    return difficultyStrings[difficulty]

register.filter('verifiedToString', verifiedToString)
register.filter('verifiedUntranslatedToString', models.verifiedUntranslatedToString)
register.filter('difficultyToString', difficultyToString)
register.filter('rarityToString', models.rarityToString)
register.filter('verificationStatusToString', models.verificationStatusToString)
register.filter('verificationUntranslatedStatusToString', models.verificationUntranslatedStatusToString)
register.filter('reportStatusToString', models.reportStatusToString)
register.filter('playWithToString', playWithToString)
register.filter('playWithToIcon', models.playWithToIcon)
register.filter('activityMessageToString', models.activityMessageToString)
register.filter('accountTabToString', models.accountTabToString)
register.filter('accountTabToIcon', models.accountTabToIcon)
register.filter('userStatusToString', models.statusToString)
register.filter('userStatusToColor', models.statusToColor)
register.filter('userStatusToColorString', models.statusToColorString)
register.filter('linkTypeToString', models.linkTypeToString)
register.filter('languageToString', languageToString)
register.filter('skillToFlaticon', skillToFlaticon)
register.filter('idolToColor', models.idolToColor)
register.filter('storedChoiceToString', models.storedChoiceToString)
register.filter('staffPermissionToString', models.staffPermissionToString)
