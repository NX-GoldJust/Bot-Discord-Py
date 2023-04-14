

#Import :
import discord, os
from discord.ext import commands
from config import *


bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

@bot.event
async def on_ready():
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{cog[:-3]}")
            except Exception as e:
                print(e)
    await bot.tree.sync()
    print(f"Bot is ready as {bot.user.name}")


bot.run(TOKEN)