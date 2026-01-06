import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    """General commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")


async def setup(bot: commands.Bot):
    """Required setup function for loading the cog."""
    await bot.add_cog(General(bot))
