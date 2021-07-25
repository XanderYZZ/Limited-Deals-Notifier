import requests
import json
import time
from plyer import notification

# Files
import RobuxFetching

# Variables to be set
cachedRobuxAmount = 0

# Constants
Webhook = "https://discord.com/api/webhooks/868962397682012211/TVbEfu6roYY2u2jw5hgne7TnKRd0kh0X9r8WOI0qxcefAnOoZI5xEf-WxtnyX5yUAhpX"
desktopNotifications = False
minimumDealPercent = 0
minuteRefresh = 5
lowerValueBound = 110000
upperValueBound = 200000

# Header
header = {
    "Cookie": ".ROBLOSECURITY=_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_E4374764BDD396D8A628A01189D40B00868E040CDB6F46A349999D1B0EB62BD86AE6A81D2155BE8953951444C3DFC25B69C7DAEDC14603B1945C6224C0FCE833EB51D02595C9D9DE4D27D5067569A18310CB0B6BEB6ABD070D0B51B7B9615A8B16124F5BDA9EC2F930B068AD8161AE970310DFB018D4D4D12E8D6608884B7C0E3092351E3178DB213B211894F2DB79F1D446FE49AC515791497765B80D35C1ED94B9AFC5E1C449B924153854865A4EE6AD77FF09B5182854D54ADC7980C7AA5CB3D02A407E8BDD7618E0F0A06A5A8C8020EFD315FCEFA5BFF6CC5458F1119830386549347BEC511B08E65F889AF971680A71F7AF4AB65B88625CA0F7E5A031684D5E7C22199959EBF49BCB5A017CD8B6416797F877E8C3B1086AD74D59BA54B138B337D81B01F9158551B8C9C57624257B429BBC73D5957CD7D3B73A4E4ED309F6E27BCA"
}

# Tables
Items = []

# Use item details instead of scraping (work on this)

# [item_name, acronym, rap, value, default_value, demand, trend, projected, hyped, rare]
cachedItemsJSON = requests.get(url="https://www.rolimons.com/itemapi/itemdetails")

cachedItemsJSON = json.loads(cachedItemsJSON.content)

cachedItemsJSON = cachedItemsJSON["items"]

#print(cachedItemsJSON["4390891467"][3])

def sendWebhook(hookContent):
    webhookData = {"content": hookContent, "title": "Testing title"}
    requests.post(Webhook, json = webhookData)

sendWebhook("Testing the message")

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
                #print("it did exist for " + str(self.itemID))
                responseData = text['data'][0]

                if 'price' in responseData:
                    best_price = responseData['price']

                self.cachedBestPrice = best_price

                return best_price
            #else:
                #print("it didn't exist for " + str(self.itemID))

    def checkForItemDeal(self):
        value = self.retrieveItemValue()
        best_price = self.retrieveBestPrice()

        if best_price and cachedRobuxAmount >= best_price:
            difference = value - best_price
            percent_deal = (difference / value)

            if percent_deal >= minimumDealPercent:
                webhookMessage = self.itemName + " selling for: " + str(best_price)

                sendWebhook(webhookMessage)

                if desktopNotifications:
                    notification.notify(
                        title = self.itemName + " Deal (" + str(round(percent_deal)) + "%)",

                        message = "Best Price: " + str(best_price),

                        timeout = 5
                    )

                    

# Constructing classes
amountOfItemsTracking = 0

for key in cachedItemsJSON:
    itemIndex = cachedItemsJSON[str(key)]

    itemName = itemIndex[0]
    value = itemIndex[3]

    if value >= lowerValueBound and value <= upperValueBound:
        Item(key, itemName)

        amountOfItemsTracking += 1

print(amountOfItemsTracking)

while True:
    cachedRobuxAmount = RobuxFetching.retrieveRobux()

    for item in Items:
        item.checkForItemDeal()

        time.sleep(1.5)

    time.sleep(60*minuteRefresh)