import discord

EMBED_COLORS = {
    "success": 0x57F287,
    "warning": 0xFEE75C,
    "error": 0xED4245,
    "info": 0x5DADE2
}

def embed_generate(type, title, description=None):
    color = EMBED_COLORS.get(type, 0x5865F2)
    return discord.Embed(title=title, description=description, color=color)

