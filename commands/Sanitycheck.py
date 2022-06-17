import discord
from command import Command

class Sanitycheck(Command):

    def __init__(self):
        super().__init__("sanitycheck", self.sanitycheck)

    async def sanitycheck(self, message):
        await message.channel.send("Howdy!")

