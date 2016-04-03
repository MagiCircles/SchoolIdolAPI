from django import template
register = template.Library()

def tier(participation, event):
    if participation.ranking:
        if participation.account_language == 'JP':
            if participation.ranking <= event.japanese_t1_rank:
                return 'T1'
            elif participation.ranking <= event.japanese_t2_rank:
                return 'T2'
        elif participation.account_language == 'EN':
            if participation.ranking <= event.english_t1_rank:
                return 'T1'
            elif participation.ranking <= event.english_t2_rank:
                return 'T2'
    return ''

register.filter('tier', tier)
