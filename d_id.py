import requests
import time
from gpt import get_d_id_keys
#from tts import speak

SOURCE_FILE = 'https://create-images-results.d-id.com/google-oauth2%7C107748073250875336091/drm_fVGk45qsU6NI5ThK_GTRQ/image.png'

key_usage=0

def wait_for_download(id):

    print("Warten auf Download...")
    url = "https://api.d-id.com/talks/" + id

    headers = {
        "accept": "application/json",
        "authorization": "Basic " + get_d_id_keys()[key_usage]
    }

    response = requests.get(url, headers=headers)

    while response.json()['status'] != "done":
        time.sleep(1)
        response = requests.get(url, headers=headers)
        print("Aktueller Status Code: " + response.json()['status'])


    print("Zum Download bereit mit den Daten: " +  response.text)

    return response.json()['result_url']

def generate_video(text):

    global key_usage
    print("Starte Generierung des Avatars...")
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "de-DE-KillianNeural"
            },
            "ssml": "false",
            "input": text
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": "https://create-images-results.d-id.com/google-oauth2%7C107748073250875336091/drm_fVGk45qsU6NI5ThK_GTRQ/image.png"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic " + get_d_id_keys()[key_usage]
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Gestartet mit Status Code: " + str(response.status_code))

    if response.status_code == 200:
        return response.json()['video_url']
    elif response.status_code == 201:
        return wait_for_download(response.json()['id'])
    elif response.status_code == 402:
        print("key aufgebraucht, verwende nächsten falls verfügbar...")
        if (key_usage + 1) < len(get_d_id_keys()):
            key_usage = key_usage + 1
            return generate_video(text)
        else:
            return None
    else:
        print(f'Error: {response.status_code}')
        speak("Oh, das ist mir jetzt aber peinlich... Mein Videoanruf zu euch scheint technische Probleme zu haben... Ich kann jetzt nur noch mit diesem alten Telefon zu euch sprechen... " + text)
        return None
