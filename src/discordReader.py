import requests
import discord
from discord.ext import commands
from discord import Client
import messageHandler

class DiscordBot(discord.Client):
    def __init__(self, messageHandler, *args, **kwargs):
        self.messageHandler = messageHandler
        super().__init__(*args, **kwargs)
        

    async def on_ready(self):
        pass


    async def on_ready(self):
        # prints succesful launch in console
        print('---\nLogged in as\nUser: ' + self.user.name + '\nID: ' + str(self.user.id) + '\n---')


    async def on_message(self, message):
        #TODO allows logout, bankpin to only come from 963799043170009098 (trusted discord plays channel)
        if message.channel.id == 963799439020007514:
            self.messageHandler.put_message("disc", message.author.name, message.content)
        elif message.channel.id == 963799043170009098:
            self.messageHandler.put_message("disc", message.author.name, message.content, False)