from discord_webhook import DiscordWebhook, DiscordEmbed

messageColor = 'dc143c'
Webhook_URL = "https://discord.com/api/webhooks/868962397682012211/TVbEfu6roYY2u2jw5hgne7TnKRd0kh0X9r8WOI0qxcefAnOoZI5xEf-WxtnyX5yUAhpX"

def sendWebhook(hookTitle, hookDescription, itemURL, imageURL, itemName):
    webhook = DiscordWebhook(url=Webhook_URL)

    # Color is decimal or hex
    embed = DiscordEmbed(title=hookTitle, url = itemURL, description=hookDescription, color=messageColor)

    embed.set_author(name=itemName, url=itemURL, icon_url=imageURL)

    # Add the embed object to the webhook
    webhook.add_embed(embed)

    response = webhook.execute()