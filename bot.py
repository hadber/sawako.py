import discord
import command 
import configparser
from os import walk
from importlib import import_module

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

client = discord.Client()
config = configparser.ConfigParser()
all_cmd = {}

@client.event
async def on_ready():
    print('Logged in as {0.user}. Hello world!'.format(client))

@client.event
async def on_message(message):
    if(message.author == client.user):
        return
    if message.content.startswith(config["BOT"]["prefix"]): # possible command
        if(message.content == ".reloadcommands"):
            if("owner_id" in config["BOT"] and not message.author.id == int(config["BOT"]["owner_id"])):
                return
            print("Requested reload of commands; processing ...")
            await message.channel.send("Reloading commands...")
            load_commands()
        if("channel" in config["BOT"] and not message.channel.id == int(config["BOT"]["channel"])): # only allow people to speak in bot-spam
            return
        else:
            cmd = message.content.split(' ')[0][1:] # element one, skipping the .
            if cmd in all_cmd:
                await all_cmd[cmd].exec(message)

def startbot():
    load_config()
    load_commands()
    client.run(config["BOT"]["token"])

def load_commands():
    # first we load all the files from commands/
    print("Loading commands...")
    commands = []
    all_cmd.clear()
    for (dirpath, dirnames, filenames) in walk("commands/"):
        commands += filenames
        break

    commands = [c[:-3] for c in commands] # remove the trailing .py

    for cmd_name in commands:
        cmd_module = import_module("commands." + cmd_name)
        try:
            cmd = getattr(cmd_module, cmd_name)
        except Exception as e:
            print(f"Couldn't load command: {cmd_name} with error: {e}")
            continue
        cmd_call = cmd_name.lower()
        all_cmd[cmd_call] = cmd()
        for aka in all_cmd[cmd_call].alias:
            all_cmd[aka] = all_cmd[cmd_call]
        print(f"Command {color(bcolors.OKGREEN, cmd_call)} loaded with aliases: {all_cmd[cmd_call].alias}")

def load_config():
    config.read("config.ini")
    print("Loaded config")

def color(color, text):
    return f"{color}{text}{bcolors.ENDC}"

startbot()