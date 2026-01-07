import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler("bot.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="A simple Discord bot with cogs"
)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guild(s)")
    
    synced = await bot.tree.sync()
    logger.info(f"Synced {len(synced)} slash command(s)")
    
    logger.info("------")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = f"cogs.{filename[:-3]}"
            await bot.load_extension(cog_name)
            logger.info(f"Loaded cog: {cog_name}")


async def main():
    async with bot:
        await load_cogs()
        token = os.getenv("DISCORD_TOKEN")
        logger.info("Starting bot...")
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
