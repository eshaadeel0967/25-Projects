import discord
from discord.ext import commands, tasks
import random
import requests

# Set up the bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # To handle new members joining

bot = commands.Bot(command_prefix="!", intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')
    # Starting a background task to check bot's status
    change_status.start()

# Event: When a new member joins the server
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f'Welcome {member.mention}! 🎉')

# Command: Get a random joke using an external API
@bot.command()
async def joke(ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = response.json()
    await ctx.send(f"{data['setup']} - {data['punchline']}")

# Command: Roll a dice with a customizable number of sides
@bot.command()
async def roll(ctx, sides: int = 6):
    """Rolls a dice with a given number of sides."""
    if sides < 2:
        await ctx.send("The dice must have at least 2 sides.")
        return
    roll_result = random.randint(1, sides)
    await ctx.send(f'You rolled a {roll_result} on a {sides}-sided dice!')

# Command: Create a simple poll
@bot.command()
async def poll(ctx, question: str, *choices: str):
    """Creates a poll with multiple choices."""
    if len(choices) < 2:
        await ctx.send("You must provide at least two choices for the poll.")
        return
    if len(choices) > 10:
        await ctx.send("You can have a maximum of 10 choices in the poll.")
        return
    
    embed = discord.Embed(title=question, description="\n".join([f"{i + 1}. {choice}" for i, choice in enumerate(choices)]), color=discord.Color.green())
    message = await ctx.send(embed=embed)
    
    for i in range(len(choices)):
        await message.add_reaction(f"{chr(127462 + i)}️")  # Add number-based reactions (🇦, 🇧, etc.)

# Command: Clear a specific number of messages (requires Manage Messages permission)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clear a specified number of messages from the chat."""
    if amount <= 0:
        await ctx.send("You must specify a positive number of messages to delete.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Deleted {len(deleted) - 1} message(s)', delete_after=5)

# Background task: Change bot status periodically
@tasks.loop(minutes=10)
async def change_status():
    statuses = [
        discord.Game("Playing with code!"),
        discord.Game("Helping you code!"),
        discord.Game("Join the server!")
    ]
    await bot.change_presence(activity=random.choice(statuses))

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing arguments: {error}")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command. Type !help to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You don't have the required permissions to execute this command.")
    else:
        await ctx.send(f"An error occurred: {error}")

# Run the bot
bot.run('YOUR_BOT_TOKEN_HERE')
