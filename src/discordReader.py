import requests
import discord
from discord.ext import commands
from discord import Client
import fileHandler

class DiscordBot(discord.Client):
    def __init__(self, commandList, messageQueue, *args, **kwargs):
        self.commandList = commandList
        self.messageQueue = messageQueue
        super().__init__(*args, **kwargs)
        

    async def on_ready(self):
        pass


    async def on_ready(self):
        # prints succesful launch in console
        print('---\nLogged in as\nUser: ' + self.user.name + '\nID: ' + str(self.user.id) + '\n---')


    async def on_message(self, message):
        #TODO allows logout, bankpin to only come from 963799043170009098 (trusted discord plays channel)
        if (message.channel.id == 963799439020007514 or message.channel.id == 963799043170009098):
            self.commandList.append(message.content)
            fileHandler.addLineToQueue("Discord: " + message.author.name + ": " + message.content, self.messageQueue)


        