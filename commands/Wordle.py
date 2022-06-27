import discord
import random
from bisect import bisect_left
from command import Command

class Wordle(Command):

    allw = []
    acceptw = []
    game_ongoing = False
    secret = ""
    guesses = 0

    def __init__(self):
        self.load_words()
        super().__init__("wordle", self.wordle, alias=["w"])

    def load_words(self):
        self.allw.clear()
        self.acceptw.clear()
        self.acceptw.extend([word.rstrip() for word in open("assets/wordle_accepted_words.txt").readlines()])
        self.allw.extend([word.rstrip() for word in open("assets/wordle_all_words.txt").readlines()])
        self.allw.extend(self.acceptw)
        self.allw.sort()
        print("COMMANDS.WORDLE: Words loaded")

    async def wordle(self, message):
        args = message.content.split(' ')
        msg_len = len(args)
#       global game_ongoing, allw, acceptw, guesses, secret

        if not msg_len >= 2:
            await message.channel.send("ERROR: bad arguments")
            return

        # someone does .wordle guess
        if args[1] == "start":
            if not msg_len == 2:
                await message.channel.send("ERROR: bad arguments (Maybe try .wordle start?)")
                return
            if not self.game_ongoing:
                self.game_ongoing = True
                self.secret = random.choice(self.acceptw)
                self.guesses = 0
                await message.channel.send("New game has started! You have 6 tries to guess the secret word!")
            else:
                await message.channel.send("Game is already ongoing, can't start a new one!")

        elif args[1] == "guess" or args[1] == "g":
            if not msg_len == 3:
                await message.channel.send("ERROR: no guess provided (Maybe try .wordle guess <your guess>?)")
                return
            if not self.game_ongoing:
                await message.channel.send("No game ongoing, start a game with .wordle start!")
                return
            guess = args[2].lower()
            pos = bisect_left(self.allw, guess)
            self.guesses += 1
            spaced_word = ""
            # we found it
            if not pos == len(self.allw) and self.allw[pos] == guess:
                correct = ""
                for idx, letter in enumerate(guess):
                    spaced_word += f":regional_indicator_{letter}:"
                    if letter in self.secret:
                        if letter == self.secret[idx]:
                            correct += "🟩"# green
                        else:
                            correct += "🟨" # yellow
                    else:
                        correct += "⬛" # black
                if correct == "🟩🟩🟩🟩🟩":
                    await message.channel.send(f"Guess {self.guesses}/6\n{spaced_word}\n{correct}\n Congrats! The word was {self.secret.upper()}")
                    self.game_ongoing = False
                else: 
                    await message.channel.send(f"Guess {self.guesses}/6\n{spaced_word}\n{correct}")
            else:
                await message.channel.send("Bad word! Try again!")
                self.guesses -= 1
            if self.guesses >= 6:
                # you lost :(
                self.game_ongoing = False
                await message.channel.send(f"Unfortunately you are out of guesses :(\n The word was {self.secret.upper()}")
                return