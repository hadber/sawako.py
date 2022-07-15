import discord
import random
import string
from command import Command
from PIL import Image, ImageChops, ImageDraw, ImageEnhance

class Meme(Command):
    
    def __init__(self):
        super().__init__("meme", self.meme)

    async def download_image(self, attachment):
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        try:
            await attachment.save(f"memes/{name}")
        except Exception as e:
            await message.channel.send(f"Failed to download attachment to memeify! (Exception: {str(e)}")
        return name
        
    async def meme(self, message):
        args = message.content.split(' ')
        if len(args) > 3:
            await message.channel.send("Bad arguments! Usage: .meme [bottom_text] <top_text>")
            return
        
        # check whether it mentions a message or if the image is inside the message
        if len(args) == 1:
            bot = "bottom text"
            top = None
        else:
            bot, *top = args[1:]
            top = top or None

        for attachment in message.attachments:
            print(attachment)
            if(attachment.content_type.startswith("image")):
                name = await self.download_image(attachment)
                self.memeify(name, bot, top)


    def memeify(self, name, bot, top):
        im = Image.open(name)
        
