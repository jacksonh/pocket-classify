
import os

import requests
from pocket import Pocket, PocketException
from google.cloud import language_v1


def classify(text, type):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=type)
    return client.classify_text(request={'document': document})


def get_text(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    return requests.get(url, headers=user_agent).text


pocket_client = Pocket(consumer_key=os.environ['POCKET_CONSUMER_KEY'],
                       access_token=os.environ['POCKET_ACCESS_TOKEN'])

pocket_client.retrieve(offset=0, count=10)
l = pocket_client.retrieve(offset=0, count=10)['list']

for key in l.keys():
    item = l[key]
    print('URL:', item['given_url'])

    c1 = classify(item['excerpt'], language_v1.Document.Type.PLAIN_TEXT)
    c2 = classify(get_text(item['given_url']), language_v1.Document.Type.HTML)

    def get_cat(cat):
        return [cat.name, cat.confidence]
    cats = [get_cat(c) for c in c1.categories] + [get_cat(c) for c in c2.categories]
    cats.sort(key=lambda c: c[1], reverse=True)
    print(cats)
