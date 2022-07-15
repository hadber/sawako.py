import discord
import random
import string
from command import Command
from PIL import Image, ImageDraw, ImageFont

class Meme(Command):
    
    def __init__(self):
        super().__init__("meme", self.meme)

    async def download_image(self, attachment):
        print("Currently downloading image.")
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        try:
            await attachment.save(f"memes/{name}")
        except Exception as e:
            await message.channel.send(f"Failed to download attachment to memeify! (Exception: {str(e)})")
        print(f"Done downloading image {name}")
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
                self.memeify(name, bot.upper(), top)
                await message.channel.send(file=discord.File(f"memes/{name}_meme.png"))

    def memeify(self, name, bot, top):
        print(f"Trying to memeify image {name}.")
        im = Image.open(f"memes/{name}")
        draw = ImageDraw.Draw(im)
        start_size = 32
        font = ImageFont.truetype("fonts/CooperHewitt-Bold.otf", start_size)
        font_size = font.getsize(bot)
        width, height = im.size

        current_use = font_size[0] / width
        newp = (start_size * 0.9) / current_use
        new_size = int(newp)
        new_font = font.font_variant(size=new_size)

        if new_size < 25:
            stroke_size = 1
        elif new_size < 50:
            stroke_size = 2
        elif new_size < 75:
            stroke_size = 3
        else:
            stroke_size = 5
        draw.text((width*0.05, height*0.05), bot, "#fff", font=new_font, stroke_width=stroke_size, stroke_fill="#000")

        im.save(f"memes/{name}_meme.png")
