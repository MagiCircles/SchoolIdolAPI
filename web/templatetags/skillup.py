from django import template
register = template.Library()

@register.filter
def ifchanged_skill_skill_level(ownedcard):
    return (ownedcard.card.skill, ownedcard.skill)
