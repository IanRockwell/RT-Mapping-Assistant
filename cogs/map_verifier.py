import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands
from io import BytesIO
import re
import json

from utils.embed_helper import *
from apis.rhythmtyper import *
from checks import run_meta_checks, run_difficulty_checks, CheckStatus

logger = logging.getLogger(__name__)


class MapVerifier(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def build_results_embed(self, title, check_results, color_override=None, description=None):
        fails = [r for r in check_results if r.status == CheckStatus.FAIL]
        warnings = [r for r in check_results if r.status == CheckStatus.WARNING]
        infos = [r for r in check_results if r.status == CheckStatus.INFO]

        if not (fails or warnings or infos):
            return None

        color = color_override or (0xED4245 if fails else 0xFEE75C if warnings else 0x57F287)
        embed = discord.Embed(title=title, description=description, color=color)

        if infos:
            info_text = "\n".join(f"ℹ️ **{r.name}**: {r.message}" for r in infos)
            embed.add_field(name="Info", value=info_text, inline=False)

        if fails:
            fail_text = "\n".join(f"❌ **{r.name}**: {r.message}" for r in fails)
            embed.add_field(name="Errors", value=fail_text, inline=False)

        if warnings:
            warn_text = "\n".join(f"⚠️ **{r.name}**: {r.message}" for r in warnings)
            embed.add_field(name="Warnings", value=warn_text, inline=False)

        return embed

    @app_commands.command(name="verifymap", description="Verify a beatmap from a URL or file attachment")
    @app_commands.describe(
        url="URL to the beatmap file",
        file="The .rtm beatmap file",
        ephemeral="Make the response only visible to you (default: False)"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        url: str = None,
        file: discord.Attachment = None,
        ephemeral: bool = False
    ):
        if not url and not file:
            embed = embed_generate(type="error", title="Missing Input", description="Please provide either a URL or attach a file to verify.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if url and file:
            embed = embed_generate(type="error", title="Too Many Inputs", description="Please provide only one input: either a URL or a file, not both.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer(ephemeral=ephemeral)

        try:
            result = None
            
            map_id = None
            
            if url:
                match = re.search(r"rhythmtyper\.net/beatmap/([a-zA-Z0-9]+)", url)
                if not match:
                    embed = embed_generate(type="error", title="Invalid URL", description="Could not extract beatmap ID from the provided URL.")
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                    return
                map_id = match.group(1)

                try:
                    zip_bytes = await fetch_beatmap(map_id)
                    result = analyze_beatmap(zip_bytes)
                except ValueError as e:
                    embed = embed_generate(type="error", title="Not Found", description=str(e))
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                    return
                except RuntimeError as e:
                    embed = embed_generate(type="error", title="Error", description=str(e))
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                    return

            elif file:
                try:
                    zip_bytes = BytesIO(await file.read())
                    result = analyze_beatmap(zip_bytes)
                except Exception:
                    embed = embed_generate(type="error", title="Invalid Map File", description="The provided file could not be parsed as a valid beatmap.")
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                    return
            
            if not result or not isinstance(result, dict) or not result.get("meta"):
                embed = embed_generate(type="error", title="Invalid Map File", description="The provided file could not be parsed as a valid beatmap.")
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            map_name = result.get("meta", {}).get("songName", "Unknown")
            mapper_name = result.get("meta", {}).get("mapper", "Unknown")
            if map_id:
                logger.info(f"{interaction.user} checked map '{map_name}' by {mapper_name} (ID: {map_id})")
            else:
                logger.info(f"{interaction.user} checked map '{map_name}' by {mapper_name} (file: {file.filename})")
            
            meta_results = run_meta_checks(result)
            meta_embed = self.build_results_embed("Mapset Verification Results", meta_results)
            
            if meta_embed:
                await interaction.followup.send(embed=meta_embed, ephemeral=ephemeral)
            else:
                embed = embed_generate(type="success", title="Mapset Checks Passed", description="No mapset-level issues found!")
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)

            difficulties = result.get("difficulties", [])
            
            for diff in difficulties:
                diff_name = diff.get("data", {}).get("name", "Unknown")
                diff_filename = diff.get("filename", "Unknown")
                drain_time_ms = calculate_drain_time(diff)
                drain_time_formatted = format_length(drain_time_ms / 1000)
                diff_description = f"Drain Time: {drain_time_formatted}\nFile Name: {diff_filename}"
                
                diff_results = run_difficulty_checks(diff)
                
                diff_embed = self.build_results_embed(f"Difficulty: {diff_name}", diff_results, description=diff_description)
                
                if diff_embed:
                    await asyncio.sleep(1)
                    await interaction.followup.send(embed=diff_embed, ephemeral=ephemeral)
                else:
                    embed = embed_generate(type="success", title=f"Difficulty: {diff_name}", description=f"{diff_description}\n\nAll checks passed!")
                    await asyncio.sleep(1)
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
        
        except Exception:
            embed = embed_generate(type="error", title="Invalid Map File", description="The provided file could not be parsed as a valid beatmap.")
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot):
    await bot.add_cog(MapVerifier(bot))
