from discord_webhook import DiscordWebhook, DiscordEmbed

messageColor = 'dc143c'
Webhook_URL = "PUT YOUR WEBHOOK URL HERE"

def sendWebhook(hookTitle, hookDescription, itemURL, imageURL, itemName):
    webhook = DiscordWebhook(url=Webhook_URL)

    # Color is decimal or hex
    embed = DiscordEmbed(title=hookTitle, url = itemURL, description=hookDescription, color=messageColor)

    embed.set_author(name=itemName, url=itemURL, icon_url=imageURL)

    # Add the embed object to the webhook
    webhook.add_embed(embed)

    response = webhook.execute()
