

# bot.py
import os
import discord
import random as rd

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user.id} has connected to Discord!\n'
    )

    members = '\n -'.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hey there {member.name}, welcome to my shitty Discord server lol!'
    )


@bot.event
async def on_message(message):

    # So it doesn't overrides any .command functions
    await bot.process_commands(message)

    if message.author == bot.user:
        return  # So the bot doesn't become recursive if it triggers any of the messages in it's messages

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


@bot.event
async def on_message_delete(message):
    if message == message:
        await message.channel.send(f'{message.author.name} deleted "{message.content}"')


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = rd.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(rd.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.command(name='clear-history', pass_context=True)
@commands.has_role('admin')
async def clear_history(ctx):
    await ctx.channel.purge(limit=99)

bot.run(TOKEN)
