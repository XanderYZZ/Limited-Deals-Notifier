import requests
import json

header = {
    "Cookie": "PUT YOUR ROBLOSECURITY HERE"
}

def retrieveRobux():
    response = requests.get(url="https://api.roblox.com/currency/balance",headers=header)

    if response.ok:
        text = response.text

        text = json.loads(text)

        robuxAmount = text['robux']

        return robuxAmount
