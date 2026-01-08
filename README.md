# RT Mapping Assistant

A Discord bot designed to assist RhythmTyper mappers with beatmap verification and tooling.

## Commands

### /map

Get info about a beatmap from a URL. Displays:

- Song title, artist, and mapper
- Length and BPM
- Ranked status and play count
- All difficulties with their star rating, OD, length, and object count

### /verifymap

Verify a beatmap for potential issues before ranking.

#### Mapset Checks

| Check | Description |
|-------|-------------|
| **Background Check** | Warns if the background image exceeds 1920x1080 or is not 16:9 aspect ratio. |
| **GDer Tags Check** | Warns if a difficulty name contains a possessive form ('s or s') but the name isn't found in the tags. |
| **Preview Point** | Fails if no preview point is set in the map metadata. |
| **Spread Requirements** | Validates drain time requirements and provides guidance on required difficulty spread based on song length. Maps under 30 seconds fail. |
| **Tags Check** | Warns if the tags field is empty. |

#### Difficulty Checks

| Check | Description |
|-------|-------------|
| **Has Notes** | Fails if the difficulty contains no notes. |
| **Hold Volume** | Warns if any held notes have a hold loop volume exceeding 70, which may be obnoxiously loud. |
| **Key Count** | Fails if more than 10 keys are pressed simultaneously at any point. |
| **OD Check** | Fails if OD is not set. Warns if OD is unusually low (below 2) or high (above 8). |

### /copyhitsounds

Copy hitsounds from one difficulty to all other difficulties in a mapset.
This is an experimental feature. The bot will return a modified `.rtm` file with hitsounds applied to all difficulties.

## Setup

### Requirements

- Python 3.10+
- Discord Bot Token

## License

See [LICENSE](LICENSE) for details.

