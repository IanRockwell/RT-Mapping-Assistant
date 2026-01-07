import re
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands
from apis.rhythmtyper import *


class MapTools(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        beatmap_match = re.search(r'rhythmtyper\.net/beatmap/([a-zA-Z0-9]+)', message.content)
        if not beatmap_match:
            return

        map_id = beatmap_match.group(1)
        
        metadata = await fetch_online_beatmap_metadata(map_id)
        
        beatmap = metadata["beatmaps"][0]
        title = beatmap["songName"]
        artist = beatmap["artistName"]
        mapper = beatmap["mapper"]
        length = beatmap["difficulties"][0]["length"]
        bpm = beatmap["bpm"]
        status = beatmap["status"]
        background_url = beatmap["backgroundImageUrl"]
        language = beatmap["language"]
        
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
            embed.add_field(name=f"{diff["name"]} | {sr:.2f} ★", value=stats, inline=True)
        
        await message.channel.send(embed=embed) 
        

async def setup(bot: commands.Bot):
    await bot.add_cog(MapTools(bot))

