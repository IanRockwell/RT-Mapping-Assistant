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
| **Background Check** | Warns if the background image exceeds 2560x1440 or is not 16:9 aspect ratio. |
| **GDer Tags Check** | Warns if a difficulty name contains a possessive form ('s or s') but the name isn't found in the tags. |
| **Genre Check** | Warns if no recognized genre tag is found in the tags field. |
| **Hitsound Consistency** | Warns if difficulties have mismatched hitsounds at the same timestamp (different sounds or one missing). |
| **Preview Point** | Fails if no preview point is set in the map metadata. |
| **Spread Requirements** | Validates drain time requirements and provides guidance on required difficulty spread based on song length. Maps under 30 seconds fail. |
| **Tags Check** | Warns if the tags field is empty. |

#### 🎯 Difficulty Checks

| Check | Description |
|-------|-------------|
| **Has Notes** | Fails if the difficulty contains no notes. |
| ~~**Hold Volume**~~ | ~~Warns if any held notes have a hold loop volume exceeding 70, which may be obnoxiously loud.~~ |
| **Key Count** | Fails if more than 10 keys are pressed simultaneously at any point. |
| **OD Check** | Fails if OD is not set. Warns if OD is unusually low (below 2) or high (above 8). |
| **Typing WPM** | Warns if any typing section requires more than 70 WPM to complete. |

### 🔊 `/copyhitsounds`

> Copy hitsounds from one difficulty to all other difficulties in a mapset

⚠️ *Experimental feature* — The bot will return a modified `.rtm` file with hitsounds applied to all difficulties.

## 🛠️ Setup

### Requirements

- Python 3.10+
- Discord Bot Token

---

<div align="center">

**📜 Licensed under the terms in [LICENSE](LICENSE)**

</div>

