import requests
import json

header = {
    "Cookie": ".ROBLOSECURITY=_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_E4374764BDD396D8A628A01189D40B00868E040CDB6F46A349999D1B0EB62BD86AE6A81D2155BE8953951444C3DFC25B69C7DAEDC14603B1945C6224C0FCE833EB51D02595C9D9DE4D27D5067569A18310CB0B6BEB6ABD070D0B51B7B9615A8B16124F5BDA9EC2F930B068AD8161AE970310DFB018D4D4D12E8D6608884B7C0E3092351E3178DB213B211894F2DB79F1D446FE49AC515791497765B80D35C1ED94B9AFC5E1C449B924153854865A4EE6AD77FF09B5182854D54ADC7980C7AA5CB3D02A407E8BDD7618E0F0A06A5A8C8020EFD315FCEFA5BFF6CC5458F1119830386549347BEC511B08E65F889AF971680A71F7AF4AB65B88625CA0F7E5A031684D5E7C22199959EBF49BCB5A017CD8B6416797F877E8C3B1086AD74D59BA54B138B337D81B01F9158551B8C9C57624257B429BBC73D5957CD7D3B73A4E4ED309F6E27BCA"
}

def retrieveRobux():
    response = requests.get(url="https://api.roblox.com/currency/balance",headers=header)

    if response.ok:
        text = response.text

        text = json.loads(text)

        robuxAmount = text['robux']

        return robuxAmount
