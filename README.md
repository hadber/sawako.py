# Sawako.py
*Simple and extendible Discord bot for all your needs!*

Installation
---------------------

To get started, install all the necessary packages using the following command. If you want to install a virtual environment, have a look [here](https://discordpy.readthedocs.io/en/stable/intro.html#virtual-environments).

```
pip install -r requirements.txt
```

Afterwards, have a look in `config.ini` to set up your bot. Instructions on how to obtain a token are found [here](https://discordpy.readthedocs.io/en/stable/discord.html).

Running
---------------------

Running the bot is as simple as:

```
python3 bot.py
```

Configuration
---------------------

An explanation of all the fields is found below. For a more concrete example, take a look at config.ini, it contains some random dummy information. (Don't worry, it's not a real token!)

```
[BOT]
token=[Your token goes here]
prefix=[The prefix used for commands]
owner_id=[ID of the owner for special bot-related commands]
channel=[Channel where you want the bot to speak]
```