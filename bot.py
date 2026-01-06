import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",  # Kept for admin commands if needed
    intents=intents,
    description="A simple Discord bot with cogs"
)


@bot.event
async def on_ready():
    """Called when the bot is ready and connected."""
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} guild(s)")
    
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash command(s)")
    
    print("------")


async def load_cogs():
    """Load all cogs from the cogs folder."""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = f"cogs.{filename[:-3]}"
            await bot.load_extension(cog_name)
            print(f"Loaded cog: {cog_name}")


async def main():
    """Main entry point for the bot."""
    async with bot:
        await load_cogs()
        token = os.getenv("DISCORD_TOKEN")
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
