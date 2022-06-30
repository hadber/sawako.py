import discord
import random
from bisect import bisect_left
from command import Command

class Wordle(Command):

    all_words = []
    accepted_words = []
    game_ongoing = False
    secret = ""
    consecutive_wins = 0
    guesses = 0
    wrong_letters = []

    def __init__(self):
        self.load_words()
        super().__init__("wordle", self.wordle, alias=["w"])

    def load_words(self):
        """ Clear word lists and combine them to one sorted list """
        self.all_words.clear()
        self.accepted_words.clear()
        self.accepted_words.extend([word.rstrip() for word in open("assets/wordle_accepted_words.txt").readlines()])
        self.all_words.extend([word.rstrip() for word in open("assets/wordle_all_words.txt").readlines()])
        self.all_words.extend(self.accepted_words)
        self.all_words.sort()

    def start_game(self):
        """ Reset all values needed for the game to start. """
        self.game_ongoing = True
        self.secret = random.choice(self.accepted_words)
        self.guesses = 0
        self.wrong_letters.clear()

    def fetch_used_letters(self):
        """ Fetch and return all used letters upon request. """
        wrong_letters = ""
        keyboard_layout = list("qwertyuiopasdfghjklzxcvbnm")
        for letter in keyboard_layout:
            if letter in self.wrong_letters:
                wrong_letters += f":black_large_square: "
            else:
                wrong_letters += f":regional_indicator_{letter}: "
            if letter in ['p', 'l']:
                wrong_letters += f"\n "
        return wrong_letters

    def create_embed(self, title=None, description=None, embed_type='error'):
        """ Create a discord embed to let sawako respond in a pretty way. """
        embed = discord.Embed()
        embed.title = title
        embed.description = description
        if embed_type == 'error':
            embed.colour = discord.Colour.red()
        elif embed_type == 'success':
            embed.colour = discord.Colour.green()
        elif embed_type == 'information':
            embed.colour = discord.Colour.blue()
        else:
            embed.colour = discord.Colour.orange()
        return embed  

    def compare_guess_with_secret(self, guess):
        """ Compare guess with the current secret and return a tuple of strings to return to the user. """
        local_secret = list(self.secret)
        correct = ""
        spaced_word = ""
        for idx, letter in enumerate(guess):
            spaced_word += f":regional_indicator_{letter}:"
            if letter in self.secret and letter in local_secret:
                if letter == self.secret[idx]:
                    correct += "🟩"# green
                else:
                    correct += "🟨" # yellow
                local_secret.remove(letter)
            else:
                if not letter in self.wrong_letters:
                    self.wrong_letters.append(letter) 
                correct += "⬛" # black
        
        return correct, spaced_word

    async def wordle(self, message):
        args = message.content.split(' ')
        message_length = len(args)

        if not message_length >= 2:
            description = "ERROR: no arguments (Maybe try `.wordle start`?)"
            embed = self.create_embed(description=description)
            await message.channel.send(content=None, embed=embed)
            return

        if args[1] == "start":
            if not message_length == 2:
                description = "ERROR: bad arguments (Maybe try `.wordle start`?)"
                embed = self.create_embed(description=description)
                await message.channel.send(content=None, embed=embed)
                return
            if not self.game_ongoing:
                self.start_game()
                description = "New game has started! You have 6 tries to guess the secret word!"
                embed = self.create_embed(embed_type='information', description=description)
                await message.channel.send(content=None, embed=embed)
            else:
                description = "Game is already ongoing, can't start a new one!"
                embed = self.create_embed(embed_type='information', description=description)
                await message.channel.send(content=None, embed=embed)
        
        elif args[1] == "guess" or args[1] == "g":
            if not message_length == 3:
                description = "ERROR: no guess provided (Maybe try `.wordle guess <your guess>`?)"
                embed = self.create_embed(description=description)
                await message.channel.send(content=None, embed=embed)
                return
            if not self.game_ongoing:
                description = "No game ongoing, start a game with `.wordle start`!"
                embed = self.create_embed(embed_type='information', description=description)
                await message.channel.send(content=None, embed=embed)
                return

            guess = args[2].lower()
            pos = bisect_left(self.all_words, guess)
            self.guesses += 1
            if self.all_words[pos] == guess:
                correct, spaced_word = self.compare_guess_with_secret(guess)
                if correct == "🟩🟩🟩🟩🟩":
                    self.consecutive_wins += 1
                    description = f"Guess {self.guesses}/6\n{spaced_word}\n{correct}\n 🥳 Congrats, {message.author.mention}! The word was {self.secret.upper()}"
                    title = f"Current Streak: {self.consecutive_wins} :fire:"
                    embed = self.create_embed(title=title, embed_type='information', description=description)
                    await message.channel.send(content=None, embed=embed)
                    self.game_ongoing = False
                    return
                else: 
                    description = f"Guess {self.guesses}/6\n{spaced_word}\n{correct}"
                    embed = self.create_embed(embed_type='information', description=description)
                    await message.channel.send(content=None, embed=embed)
            else:
                description = "Bad word! Try again!"
                embed = self.create_embed(embed_type='information', description=description)
                await message.channel.send(content=None, embed=embed)
                self.guesses -= 1
                
            if self.guesses >= 6:
                self.game_ongoing = False
                description = f"Unfortunately you are out of guesses :(\n The word was {self.secret.upper()}"
                embed = self.create_embed(description=description)
                self.consecutive_wins = 0
                await message.channel.send(content=None, embed=embed)
                return
                
        elif args[1] == "used":
            wrong_letters_in_keyboard_layout = self.fetch_used_letters()
            description = f"The solution is made up of the following letters: \n{wrong_letters_in_keyboard_layout}"
            embed = self.create_embed(embed_type='information', description=description)
            await message.channel.send(content=None, embed=embed)
