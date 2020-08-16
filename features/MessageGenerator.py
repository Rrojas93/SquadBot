import requests, json, random, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def getInsult():
    response = requests.get('https://www.rappad.co/api/battles/random_insult')
    insult = json.loads(response.text)
    return insult['insult']

def getCompliment():
    with open(os.path.join(BASE_DIR, 'assets', 'text_data', 'extractedCompliments.txt'), 'r', encoding='utf-8') as f:
        compliments = f.read()
    compliments = compliments.splitlines()
    randChoice = random.randint(0, len(compliments))
    return compliments[randChoice].strip()


print(getCompliment())