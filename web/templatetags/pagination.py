from django import template
import re

register = template.Library()

def cleanpage(current_url):
    current_url = re.sub(r'(\?page=\d+)', r'?', current_url)
    current_url = re.sub(r'(\?\&)', r'?', current_url)
    current_url = re.sub(r'(\&page=\d+)', r'', current_url)
    return current_url

def nextpage(current_url, page_number):
    return cleanpage(current_url) + 'page=' + str(page_number + 1)
register.filter('nextpage', nextpage)

def previouspage(current_url, page_number):
    return cleanpage(current_url) + 'page=' + str(page_number - 1)
register.filter('previouspage', previouspage)
