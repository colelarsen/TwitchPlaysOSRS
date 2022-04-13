import requests
import discord
from discord.ext import commands
from discord import Client

class DiscordBot(discord.Client):
    def __init__(self, commandList, *args, **kwargs):
        self.commandList = commandList
        super().__init__(*args, **kwargs)
        

    async def on_ready(self):
        pass


    async def on_ready(self):
        # prints succesful launch in console
        print('---\nLogged in as\nUser: ' + self.user.name + '\nID: ' + str(self.user.id) + '\n---')


    async def on_message(self, message):
        if (message.channel.id == 963799439020007514 or message.channel.id == 963799043170009098):
            self.commandList.append(message.content)


        