from django import template
import redis
import json

register = template.Library()

red = redis.Redis(
    host = 'redis-18308.c238.us-central1-2.gce.cloud.redislabs.com',
    port = 18308,
    password = 'ljLCe2nxalVGsAtde9nHglLiZJVMFVS7'
)

@register.filter(name = 'censor')
def censor(text):
    bad_words = json.loads(red.get('bad_words'))
    text = text.split(' ')
    bwords_count = 0

    for index, word in enumerate(text):

        if len(word) > 2:

            if word.lower() in bad_words:
                text[index] = '**censored**:D'
                bwords_count += 1

    return ' '.join(map(str, text))

@register.filter(name = 'index')
def index(list, i):
    return list[i]