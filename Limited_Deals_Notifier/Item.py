import requests
import json
import time
from plyer import notification

# Files
import RobuxFetching
import Webhook

# Variables to be set
cachedRobuxAmount = 0

# Constants
desktopNotifications = False
minimumDealPercent = 20
timeBetweenItem = 0.1
refreshTime = 60 # Amount of seconds until the while loop starts again
lowerValueBound = 6000
upperValueBound = 20000

# Header
header = {
    "Cookie": "PUT YOUR ROBLOSECURITY HERE"
}

# Tables
Items = []

# [item_name, acronym, rap, value, default_value, demand, trend, projected, hyped, rare]
def retrieveItemsJSON():
    cachedItemsJSON = requests.get(url="https://www.rolimons.com/itemapi/itemdetails")

    cachedItemsJSON = json.loads(cachedItemsJSON.content)

    cachedItemsJSON = cachedItemsJSON["items"]

    return cachedItemsJSON

cachedItemsJSON = retrieveItemsJSON()

class Item:
    def __init__(self, itemID, itemName):
        self.itemID = itemID
        self.itemName = itemName

        Items.append(self)
    
    def retrieveItemValue(self):
        self.cachedValue = cachedItemsJSON[str(self.itemID)][3]

        return self.cachedValue

    def retrieveBestPrice(self):
        response = requests.get(url='https://economy.roblox.com/v1/assets/'+ str(self.itemID) +'/resellers', headers=header)

        if response.ok:
            text = json.loads(response.text)

            best_price = 0

            if text['data']:
                responseData = text['data'][0]

                if 'price' in responseData:
                    best_price = responseData['price']

                self.cachedBestPrice = best_price

                return best_price

    def checkForItemDeal(self):
        value = self.retrieveItemValue()
        best_price = self.retrieveBestPrice()

        if best_price and cachedRobuxAmount >= best_price:
            difference = value - best_price
            percent_deal = (difference / value) * 100 # Multiplied by 100 because it represents a percentage so it needs to be

            if percent_deal >= minimumDealPercent:
                hookTitle = self.itemName + " Deal (" + str(round(percent_deal, 2)) + "%)"
                desc = self.itemName + " selling for: " + "{:,}".format(best_price)

                itemURL = "https://www.roblox.com/catalog/" + self.itemID
                imageURL = "https://www.roblox.com/asset-thumbnail/image?assetId=" + self.itemID + "&width=420&height=420&format=png"

                Webhook.sendWebhook(hookTitle, desc, itemURL, imageURL, self.itemName)

                if desktopNotifications:
                    notification.notify(
                        title = hookTitle,

                        message = desc,

                        timeout = 5
                    )


# Constructing classes
def declareClasses():
    Items.clear()

    for key in cachedItemsJSON:
        itemIndex = cachedItemsJSON[str(key)]

        itemName = itemIndex[0]
        value = itemIndex[3]

        if value >= lowerValueBound and value <= upperValueBound:
            Item(key, itemName)

while True:
    cachedItemsJSON = retrieveItemsJSON()
    cachedRobuxAmount = RobuxFetching.retrieveRobux()

    # Retrieve the items
    declareClasses()

    for item in Items:
        item.checkForItemDeal()

        time.sleep(timeBetweenItem)

    time.sleep(refreshTime)
