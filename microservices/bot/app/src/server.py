from src import app
from flask import jsonify, request
import requests
import json
import os
import re

adminId = os.environ['ADMIN_ID']
accessToken = os.environ['ACCESS_TOKEN']
translateApiKey = os.environ['TRANSLATE_API_KEY']


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
        translationObj = translate("en", msgBody[3:-5])
        translation = translationObj["translatedText"]
        lang = translationObj["detectedSourceLanguage"]
        if (lang != "en"):
            response = buildNote(msgBody[3:-5], lang, translation)
            sendNote(convId, response)

    if (topic == "conversation.user.created"):
        msgBody = input["data"]["item"]["conversation_message"]["body"]
        translationObj = translate("en", msgBody[3:-5])
        translation = translationObj["translatedText"]
        lang = translationObj["detectedSourceLanguage"]
        if (lang != "en"):
            response = buildNote(msgBody[3:-5], lang, translation)
            sendNote (convId, response)


    if (topic == "conversation.admin.noted"):
        msgArray = input["data"]["item"]["conversation_parts"]["conversation_parts"]
        for msg in msgArray:
            msgBody = msgBody + msg["body"] + " "
        text = msgBody[3:-5]
        regex = r"(\/translate)\ ([^\s]+)\ (.*)"
        match = re.search(regex, text)
        if (match.group(1) == '/translate'):
            translationObj = translate(match.group(2), match.group(3))
            translation = translationObj["translatedText"]
            sendMessage(convId, translation)
    return "OK"


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
    translationObj = respObj["data"]["translations"][0]
    return translationObj

def buildNote(message, lang, translation):
    response = "Original Message: "+message+ "\nLanguage Code: "+lang+"\nTranslation: " + translation + "\n\n To reply in the same language, please add a note of the format '/translate language_code sentence'\nExample: /translate fr How can I help you?"
    return response


def sendNote(convId, message):
    url = "https://api.intercom.io/conversations/" + convId + "/reply"
    bearer = "Bearer " + accessToken
    headers = {
        "Authorization": bearer,
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "body": message ,
        "type": "admin",
        "admin_id": adminId,
        "message_type": "note"
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    respObj = r.json()
    print ("Send Note Responce: ")
    print (respObj)
    print ("==========================================================================")

def sendMessage(convId, message):
    url = "https://api.intercom.io/conversations/" + convId + "/reply"
    bearer = "Bearer " + accessToken
    headers = {
        "Authorization": bearer,
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "body": message ,
        "type": "admin",
        "admin_id": adminId,
        "message_type": "open"
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    respObj = r.json()
    print ("Send Message Responce: ")
    print (respObj)
    print ("==========================================================================")
