import discord
import requests
from datetime import datetime
from command import Command

class Urban(Command):
    
    def __init__(self):
        super().__init__("urban", self.urban)

    async def urban(self, message):

        if len(message.content.split(' ')) < 2:
            await message.channel.send("Bad arguments! Usage: .urban <word or phrase>")
            return
        term = '+'.join(message.content.split(' ')[1:])
        url = "http://api.urbandictionary.com/v0/define?term=" + term
        
        req = requests.get(url)
        resp = req.json()
        definition = resp["list"][0]["definition"]

        em = discord.Embed()
        em.title = term.replace("+", " ")
        em.description = definition.replace("[", "").replace("]", "")
        em.colour = discord.Colour.orange()
        em.set_footer(text = "Urban Dictionary", icon_url = "https://i.imgur.com/MT8f7hU.png")
 #       em.set_image(url = "https://i.imgur.com/MT8f7hU.png")
        em.timestamp = datetime.now()

        await message.channel.send(content=None, embed=em)