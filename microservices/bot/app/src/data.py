import requests
import json

dataUrl = 'http://data.hasura/v1/query'

headers = {
    'X-Hasura-Role': 'admin',
    'X-Hasura-User-Id': "1",
    'Content-Type': 'application/json'
}

def checkTranslateMode(convId):
    payload = {
        "type": "select",
        "args": {
            "table": "translate_mode",
            "columns": [
                "language"
            ],
            "where": {
                "conversation_id": convId
            }
        }
    }

    r = requests.post(url=dataUrl, headers=headers, data=json.dumps(payload))
    respObj = r.json()
    if (len(respObj) == 0):
        return 'none'

    return respObj[0]["language"]


def turnOffTranslate(convId):
    payload = {
        "type": "delete",
        "args": {
            "table": "translate_mode",
            "where": {
                "conversation_id": convId
            }
        }
    }

    r = requests.post(url=dataUrl, headers=headers, data=json.dumps(payload))
    respObj = r.json()

def updateLanguageMode(convId, lang):
    sqlString =  "INSERT INTO translate_mode (conversation_id, language) VALUES ({cId}, '{l}') ON CONFLICT (conversation_id) DO UPDATE SET language = '{l}'".format(cId = str(convId), l = lang)
    print ("SQLString")
    print (sqlString)
    payload = {
        "type": "run_sql",
        "args": {
            "sql": sqlString
        }
    }

    r = requests.post(url=dataUrl, headers=headers, data=json.dumps(payload))
    respObj = r.json()
    print ("Update/Insert Response: ")
    print (respObj)
