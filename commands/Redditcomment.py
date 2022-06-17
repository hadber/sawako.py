import discord
import requests
from datetime import datetime
from command import Command

class Redditcomment(Command):

    def __init__(self):
        super().__init__("redditcomment", self.redditcomment, alias=['rc', 'comment'])

    async def redditcomment(self, message):
        if len(message.content.split(' ')) != 2:
            await message.channel.send("Bad arguments! Usage: .redditcomment <subreddit>")
            return
        subreddit = message.content.split(' ')[1]
        r = requests.get(f'https://www.reddit.com/r/{subreddit}/comments.json?limit=1', headers = {'User-agent': 'funnybot'})
        comment = r.json()

        if "error" in comment or comment["data"]["after"] is None: 
            await message.channel.send(f'No such subreddit: {subreddit}')
        else:
            to_send = comment["data"]["children"][0]["data"]["body"]
            to_send = to_send if len(to_send) < 5000 else "Damn this comment is too long lol"
            
            em = discord.Embed()
            em.description = to_send
            em.colour = discord.Colour.orange()
            em.set_footer(text = "/r/" + subreddit)
            em.timestamp = datetime.now()

            await message.channel.send(content=None, embed=em)