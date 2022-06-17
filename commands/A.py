import discord
import random
from command import Command

class A(Command):
    
    def __init__(self):
        super().__init__("a", self.a)

    async def a(self, message):
        to_send = ''
        case = 'nothing'
        if len(message.content.split(' ')) == 2:
            case = message.content.split(' ')[1]
        if(case.lower() == 'caps'):
            to_send = "A" * random.randint(1, 128)
        elif(case.lower() == 'nocaps'):
            to_send = "a" * random.randint(1, 128)
        else:
            for i in range(random.randint(1, 128)):
                to_send += "A" if bool(random.getrandbits(1)) else "a"
        await message.channel.send(to_send)