import requests
import json
import os

from . import intercom

translateApiKey = os.environ['TRANSLATE_API_KEY']


def translate(lang, text):
    translateUrl = "https://translation.googleapis.com/language/translate/v2?key="+translateApiKey
    payload = {
        "q": text,
        "target": lang
    }

    r = requests.post(url=translateUrl, data=json.dumps(payload))
    respObj = r.json()
    print ("Translate Response: ")
    print (respObj)
    print ("==========================================================================")
    return respObj
