import logging
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

