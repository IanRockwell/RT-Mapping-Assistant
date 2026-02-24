<div align="center">

# 🎹 RT Mapping Assistant

**A Discord bot designed to assist [RhythmTyper](https://rhythmtyper.net/) mappers with beatmap verification and tooling.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord](https://img.shields.io/badge/Discord_OAuth-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1458240749664473160)
[![License](https://img.shields.io/badge/License-See_File-green?style=for-the-badge)](LICENSE)

</div>

<br>

## ⚡ Commands

### 📋 `/map`

> Get info about a beatmap from a URL

**Displays:**

- Song title, artist, and mapper
- Length and BPM
- Ranked status and play count
- All difficulties with their star rating, OD, length, and object count

### ✅ `/verifymap`

> Verify a beatmap for potential issues before ranking

#### 🗂️ Mapset Checks

| Check | Description |
|-------|-------------|
| **BG** | Warns if the background image exceeds 2560x1440 or is not 16:9 aspect ratio. |
| **GDer** | Warns if a difficulty name contains a possessive form ('s or s') but the name isn't found in the tags. |
| **Genre** | Warns if no recognized genre tag is found in the tags field. |
| **HS Inconsistency** | Warns if difficulties have mismatched hitsounds at the same timestamp (different sounds or one missing). |
| **Language** | Fails if the map's set language is not found in the tags. Warns if language is set to "Other" to ensure the correct language is in the tags. |
| **Preview** | Fails if no preview point is set in the map metadata. |
| **Spread** | Validates drain time requirements and provides guidance on required difficulty spread based on song length. Maps under 30 seconds fail. |
| **Tags** | Warns if the tags field is empty. |
| **Unicode** | Fails if artistName or songName contain Unicode characters. Romanized fields should only contain ASCII. |

#### 🎯 Difficulty Checks
| Check | Description |
|-------|-------------|
| **Notes** | Fails if the difficulty contains no notes. |
| **Keys** | Fails if more than 10 keys are pressed simultaneously at any point. |
| **OD** | Fails if OD is not set. Warns if OD is unusually low (below 2) or high (above 8). |
| **Snap** | Fails if any notes are not snapped to a standard beat division (1/1 through 1/16). |
| **WPM** | Warns if any typing section requires more than 80 WPM to complete. |
| ~~**Hold**~~ | ~~Warns if any held notes have a hold loop volume exceeding 70, which may be obnoxiously loud.~~ |

### 🔊 `/copyhitsounds`

> Copy hitsounds from one difficulty to all other difficulties in a mapset

⚠️ *Experimental feature* — The bot will return a modified `.rtm` file with hitsounds applied to all difficulties.

## 🛠️ Setup

### Requirements

- Python 3.10+
- Discord Bot Token

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

## 🤝 Contributing

Feel free to open a PR!

---

<div align="center">

**📜 Licensed under the terms in [LICENSE](LICENSE)**

</div>

