import discord
from command import Command

class Testcommand(Command):
    
    def __init__(self):
        super().__init__("sanitycheck", self.testcommand)

    async def testcommand(self, message):
        em = discord.Embed()
        em.title = "This is an embed test"
        await message.channel.send(content=None, embed=em)