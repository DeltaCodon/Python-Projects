

# bot.py
import os
import discord
import random as rd

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = "!", intents = intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user.id} has connected to Discord!\n'
    )
   
    members = '\n -'.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hey there {member.name}, welcome to my shitty Discord server lol!'
    )

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    automatedResponse = [
        "Thank you for replying... You're a doodoo head aha\n get rekt nerd",
        "Hey what's up",
        ("Why are you talking to me, loser?"),
                         ]

    if message.content.lower() == 'hi' or message.content.lower() == 'hello':
        repsonse = rd.choice(automatedResponse)
        await message.channel.send(repsonse)
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')


@client.event
async def on_message_delete(message):
    if message == message:
        await message.channel.send(f'{message.author.name} deleted "{message.content}"')
    


client.run(TOKEN)