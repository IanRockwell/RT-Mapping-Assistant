import logging
import re
from datetime import datetime
from io import BytesIO
import discord
from discord import app_commands
from discord.ext import commands
from apis.rhythmtyper import *
from utils.embed_helper import embed_generate
from tools.hitsound_copier import copy_hitsounds

logger = logging.getLogger(__name__)


class MapTools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="map", description="Get info about a beatmap from a URL")
    @app_commands.describe(url="URL to the beatmap")
    async def map_info(self, interaction: discord.Interaction, url: str):
        match = re.search(r"rhythmtyper\.net/beatmap/([a-zA-Z0-9]+)", url)
        if not match:
            embed = embed_generate(
                type="error",
                title="Invalid URL",
                description="Could not extract beatmap ID from the provided URL."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer()

        map_id = match.group(1)

        try:
            metadata = await fetch_online_beatmap_metadata(map_id)
        except ValueError as e:
            embed = embed_generate(type="error", title="Not Found", description=str(e))
            await interaction.followup.send(embed=embed)
            return
        except RuntimeError as e:
            embed = embed_generate(type="error", title="Error", description=str(e))
            await interaction.followup.send(embed=embed)
            return

        if not metadata.get("beatmaps"):
            embed = embed_generate(type="error", title="Not Found", description="No beatmap found with that ID.")
            await interaction.followup.send(embed=embed)
            return

        beatmap = metadata["beatmaps"][0]
        title = beatmap["songName"]
        artist = beatmap["artistName"]
        mapper = beatmap["mapper"]
        length = beatmap["difficulties"][0]["length"]
        bpm = beatmap["bpm"]
        status = beatmap["status"]
        background_url = beatmap["backgroundImageUrl"]

        plays = beatmap["playCount"]

        if status == "ranked":
            date_str = beatmap["rankedDate"]
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            date_text = f"Ranked {date.strftime('%b %d, %Y')}"
        else:
            last_updated = beatmap["lastUpdatedAt"]
            date = datetime.fromtimestamp(last_updated["_seconds"])
            date_text = f"Updated {date.strftime('%b %d, %Y')}"

        embed = discord.Embed(
            title=f"{artist} - {title} by {mapper}",
            description=f"Length: {format_length(length)} | BPM: {bpm}",
            url=url,
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=background_url)
        embed.set_footer(text=f"{status.capitalize()} | {plays} plays | {date_text}")

        difficulties = beatmap["difficulties"]
        sorted_diffs = sorted(difficulties, key=lambda d: d.get("starRating", 0), reverse=True)
        for diff in sorted_diffs:
            sr = diff.get("starRating", 0)
            od = diff.get("overallDifficulty", 0)
            diff_length = diff.get("length", 0)
            objects = diff.get("noteCount", 0) + diff.get("holdCount", 0)

            stats = (
                f"- OD: {od:.2f}\n- Length: {format_length(diff_length)}\n- Objects: {objects}"
            )
            embed.add_field(name=f"{diff['name']} | {sr:.2f} ★", value=stats, inline=True)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="copyhitsounds", description="Copy hitsounds from one difficulty to all others")
    @app_commands.describe(
        file="The .rtm beatmap file",
        source_difficulty="Name of the difficulty to copy hitsounds from",
        ignore_tapvolumes="Ignore tap note volumes and hold start/end volumes (default: False)",
        ignore_holdvolumes="Ignore hold note loop volumes (default: False)"
    )
    async def hitsounds_copy(
        self,
        interaction: discord.Interaction,
        file: discord.Attachment,
        source_difficulty: str,
        ignore_tapvolumes: bool = False,
        ignore_holdvolumes: bool = False
    ):
        if not file.filename.endswith('.rtm'):
            embed = embed_generate(
                type="error",
                title="Invalid File",
                description="Please provide a valid `.rtm` file."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            zip_bytes = BytesIO(await file.read())
            output, stats = copy_hitsounds(zip_bytes, source_difficulty, ignore_tapvolumes, ignore_holdvolumes)
            
            output_filename = file.filename.replace('.rtm', '_hitsounded.rtm')
            
            embed = embed_generate(
                type="success",
                title="Hitsounds Copied",
                description=(
                    f"Copied hitsounds from **{stats['source_name']}** to all other difficulties.\n\n"
                    f"**Modified:** {stats['modified_notes']} notes\n"
                    f"**Difficulties:** {stats['target_difficulties']}\n\n"
                    f"❗This feature is __experimental__. Be sure to double check the hitsounds. ❗"
                )
            )
            await interaction.followup.send(
                embed=embed,
                file=discord.File(output, filename=output_filename),
                ephemeral=True
            )
            
        except Exception as e:
            embed = embed_generate(
                type="error",
                title="Hitsound Copy Failed",
                description=str(e)
            )
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(MapTools(bot))

