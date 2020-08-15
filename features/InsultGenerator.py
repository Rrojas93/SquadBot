import requests, json

def getInsult():
    response = requests.get('https://www.rappad.co/api/battles/random_insult')
    insult = json.loads(response.text)
    return insult['insult']
