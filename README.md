<div align="center">

# RT Mapping Assistant

**A Discord bot designed to assist [RhythmTyper](https://rhythmtyper.net/) mappers with beatmap verification and tooling.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord](https://img.shields.io/badge/Discord_OAuth-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1458240749664473160)
[![License](https://img.shields.io/badge/License-See_File-green?style=for-the-badge)](LICENSE)

</div>

<br>

## Commands

### `/verifymap`

> Verify a beatmap for potential issues before ranking

#### Mapset Checks

| Check | Description |
|-------|-------------|
| **BG** | Warns if the background image exceeds 2560x1440. |
| **GDer** | Warns if a difficulty name contains a possessive form ('s or s') but the name isn't found in the tags. |
| **Genre** | Warns if no recognized genre tag is found in the tags field. |
| **HS Inconsistency** | Warns if difficulties have mismatched hitsounds at the same timestamp (different sounds or one missing). |
| **Language** | Fails if the map's set language is not found in the tags. Warns if language is set to "Other" to ensure the correct language is in the tags. |
| **Preview** | Fails if no preview point is set in the map metadata. |
| **Spread** | Validates drain time requirements and provides guidance on required difficulty spread based on song length. Maps under 30 seconds fail. |
| **Tags** | Warns if the tags field is empty. |
| **Unicode** | Fails if artistName or songName contain Unicode characters. Romanized fields should only contain ASCII. |
| **Audio Quality** | Warns if the audio appears overencoded. Spectral analysis suggesting a significantly lower quality than the file's declared bitrate (gap of 64+ kbps). |

#### Difficulty Checks
| Check | Description |
|-------|-------------|
| **Notes** | Fails if the difficulty contains no notes. |
| **Time Order** | Fails if any hold note or typing section has an end time that is not after its start time. |
| **Chord Alignment** | Fails if notes (taps, hold starts, or hold ends) are within 2ms of each other without being exactly aligned, which can break snap coloring. |
| **Key Overlap** | Fails if two or more notes share the same key at the same time, including taps during an active hold or notes within the 2ms tolerance window. |
| **Keys** | Fails if more than 10 keys are pressed simultaneously at any point. |
| **OD** | Fails if OD is not set. Warns if OD is unusually low (below 2) or high (above 8). |
| **Snap** | Fails if notes aren't snapped to 1/1–1/32. Warns on uncommon divisions (1/5, 1/7, 1/12, 1/16, 1/32). |
| **WPM** | Warns if any typing section requires more than 80 WPM to complete. |
| **Drain Coverage** | Fails if drain time is less than 60% of the total audio file length. |
| **Hold** | Warns on loud hold loop volumes above 60%. If more than 40% of hold notes are above 60%, it gives a summary warning; otherwise, it attaches timestamps for the affected holds so you can confirm they are intentional. |

### `/copyhitsounds`

> Copy hitsounds from one difficulty to all other difficulties in a mapset

*Experimental feature* — The bot will return a modified `.rtm` file with hitsounds applied to all difficulties.

### `/shiftnotes`

> Shift all notes in a mapset by a given number of milliseconds

The bot will return a modified `.rtm` file with note timings shifted.

## Setup

### Requirements

- Python 3.10+
- Discord Bot Token
- [ffmpeg](https://ffmpeg.org/download.html) (optional, but it's required for spectral audio quality detection)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/IanRockwell/RT-Mapping-Assistant.git
   cd RT-Mapping-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root with your Discord bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Contributing

Feel free to open a PR!

---

<div align="center">

**Licensed under the terms in [LICENSE](LICENSE)**

</div>
