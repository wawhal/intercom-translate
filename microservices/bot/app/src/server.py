from src import app
from flask import jsonify, request

from . import intercom
from . import googleTranslate
from . import data

import requests
import json
import os
import re



@app.route("/")
def main():
    return "Intercom bot is running"

@app.route("/bot", methods=['POST'])
def bot():
    KEY = str("secret")
    DATA = request.get_data()
    input = json.loads(DATA.decode())
    topic = input["topic"]
    convId = input["data"]["item"]["id"]
    print ("Request Body: ")
    print (input)
    print ("==========================================================================")
    msgBody = ""
    if(topic == "conversation.user.replied"):
        msgArray = input["data"]["item"]["conversation_parts"]["conversation_parts"]
        for msg in msgArray:
            msgBody = msgBody + msg["body"] + " "
        translationObj = googleTranslate.translate("en", msgBody[3:-5])
        translation = translationObj["translatedText"]
        lang = translationObj["detectedSourceLanguage"]
        if (lang != "en"):
            response = intercom.buildNote(msgBody[3:-5], lang, translation)
            intercom.sendNote(convId, response)

    if (topic == "conversation.user.created"):
        msgBody = input["data"]["item"]["conversation_message"]["body"]
        translationObj = googleTranslate.translate("en", msgBody[3:-5])
        translation = translationObj["translatedText"]
        lang = translationObj["detectedSourceLanguage"]
        if (lang != "en"):
            response = intercom.buildNote(msgBody[3:-5], lang, translation)
            intercom.sendNote (convId, response)


    if (topic == "conversation.admin.noted"):
        msgArray = input["data"]["item"]["conversation_parts"]["conversation_parts"]
        for msg in msgArray:
            msgBody = msgBody + msg["body"] + " "
        text = msgBody[3:-5]
        langMode = data.checkTranslateMode(convId)
        regex = r"(\/translate)\ (.*)"
        match = re.search(regex, text)
        if (match and match.group(1) == '/translate'):
            if (match.group(2) == 'off'):
                data.turnOffTranslate(convId)
            else:
                data.updateLanguageMode(convId, match.group(2))
                infoNote = "You are in language mode '" + match.group(2) + "'.Please make an internal note saying '/translate off' to turn it off."
                intercom.sendNote(convId, infoNote)
        else:
            if (langMode != 'none'):
                translationObj = googleTranslate.translate(match.group(2), match.group(3))
                translation = translationObj["translatedText"]
                intercom.sendMessage(convId, translation)

    return "OK"


