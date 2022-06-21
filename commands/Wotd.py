import discord
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from command import Command

class Wotd(Command):
    
    wotd_embed = None
    wotd_timestamp = None

    def __init__(self):
        super().__init__("wotd", self.wotd)


    async def wotd(self, message):
        """ Embeds the word of the day in the channel. """
        if self.wotd_timestamp is None or self.wotd_timestamp.date() < datetime.today().date():
            self.construct_embed()
        await message.channel.send(content=None, embed=self.wotd_embed)


    def construct_embed(self):
        """ Constructs an embed based on the word of the day by Merriam Webster. """
        result = requests.get("https://www.merriam-webster.com/word-of-the-day")
        soup = BeautifulSoup(result.text, 'html.parser')

        wotd_container = soup.find("div", {"class": "wod-definition-container"})
        all_ps = wotd_container.findAll("p")
        definition, *usages = all_ps
        definition = definition.get_text()
        usage = ""
        for usage_candidate in usages: 
            if usage_candidate.get_text().startswith('//'):
                usage += usage_candidate.get_text() + '\n'

        wotd_examples = wotd_container.find("div", {"class": "left-content-box"})
        word_in_context = wotd_examples.find("p").get_text()

        did_you_know_wrapper = soup.find("div", {"class": "did-you-know-wrapper"})
        did_you_know = did_you_know_wrapper.find("p").get_text()

        word_of_the_day_div = soup.find("div", {"class": "word-and-pronunciation"})
        word_of_the_day = word_of_the_day_div.find("h1").get_text()

        self.wotd_timestamp = datetime.now()

        self.wotd_embed = discord.Embed()
        self.wotd_embed.title = word_of_the_day
        self.wotd_embed.add_field(name="Definition", value="\n".join([definition,usage]), inline=False)
        self.wotd_embed.add_field(name="Usage in context", value=word_in_context, inline=False)
        self.wotd_embed.add_field(name="Did you know?", value=did_you_know, inline=False)
        self.wotd_embed.colour = discord.Colour.blue()
        self.wotd_embed.set_footer(text="Word of the day", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Merriam-Webster_logo.svg/240px-Merriam-Webster_logo.svg.png")
        self.wotd_embed.timestamp = datetime.today()
