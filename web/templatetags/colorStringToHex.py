from django import template
register = template.Library()

colors = {
    'Smile': '#e6006f',
    'Pure': '#20ab53',
    'Cool': '#0098eb',
    'All': '#8f56cc',    
}

def colorStringToHex(value):
    if value in colors:
        return colors[value]
    return colors['Smile']

register.filter('colorStringToHex', colorStringToHex)
