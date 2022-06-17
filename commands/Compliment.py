import discord
import requests
import sched, time
import random
from command import Command

class Compliment(Command):

    compliment_scheduler = sched.scheduler(time.time, time.sleep)
    compliments = []

    def __init__(self):
        self.load_compliments()
        super().__init__("compliment", self.compliment)

    async def compliment(self, message):
        #r = requests.get('https://www.reddit.com/r/gonewild/comments.json?limit=100', headers = {'User-agent': 'funnybot'})
        #comments = r.json()
        #print(comments)

        if(len(message.mentions) != 1):
            await message.channel.send("You need to compliment one person! Usage: .compliment @user")
            return
        if len(message.content.split(' ')) != 2:
            await message.channel.send("Bad arguments! Usage: .compliment @user")
            return
        user_mentioned = message.mentions[0]

        await message.channel.send(user_mentioned.mention + ", " + self.compliments[random.randint(0, 99)])

        if(not self.compliment_scheduler.empty()):
            for ev in self.compliment_scheduler.queue:
                self.compliment_scheduler.cancel(ev)
        # remove them all then add it again to scheduler
        self.compliment_scheduler.enter(1800, 1, self.load_compliments)

    def load_compliments(self):
        print("Compliments are being loaded")
        self.compliments.clear()
        r = requests.get('https://www.reddit.com/r/gonewild/comments.json?limit=100', headers = {'User-agent': 'funnybot'})
        all_comments = r.json()
        for child in all_comments["data"]["children"]:
            self.compliments.append(child["data"]["body"])

    #https://www.reddit.com/r/gonewild/comments.json?limit=100