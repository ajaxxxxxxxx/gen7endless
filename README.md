# Gen 7 Endless Battle Facility

A **prototype** local single-player battle facility built around Pokémon Showdown, with a Python AI opponent and per-format streak tracking.

## Formats

| Key | Format | Team |
| --- | --- | --- |
| `bh4` | Gen 7 Balanced Hackmons Doubles | Bring six, select four |
| `bh6` | Gen 7 Balanced Hackmons Doubles | Bring six, use six |
| `lc3` | Gen 7 Little Cup Singles | Bring six, select three |
| `lc6` | Gen 7 Little Cup Singles | Bring six, use six |

Custom format definitions live in `showdown-config/custom-formats.ts`, inheriting the historic Gen 7 Showdown formats and restrictions. Curated AI teams are stored in `teams/`.

## Setup (prototype)

1. Install Node.js and Python, then clone the official [Pokémon Showdown](https://github.com/smogon/pokemon-showdown) server and this repository.
2. From this repository, run `python scripts/install_showdown.py /path/to/pokemon-showdown`. This copies custom formats into the server without overwriting an existing custom-format file.
3. Build and run Showdown using its upstream instructions. For local experiments, configure the server to accept localhost connections and do not expose an insecure server to the internet.
4. Install Python dependencies with `python -m pip install -r requirements.txt`.
5. In this repository, run `python -m facility.bot --format bh4 --human YOUR_SHOWDOWN_USERNAME`, substituting your nickname and desired format key.
6. Connect a compatible locally hosted Showdown client and challenge `MaisonAI`.

## Validation

- Local core tests: `python -m unittest discover -s tests`
- After building Showdown, copy `scripts/verify_formats.cjs` and `scripts/verify_teams.cjs` into the Showdown root, then run `node verify_formats.cjs` and `node verify_teams.cjs /path/to/gen7endless`.

## Current limitations

This is a starter implementation, **not yet an independently verified playable release**. The AI adapter and custom formats have not been tested end-to-end against the currently installed upstream Showdown and poke-env versions. There is no bundled local browser client, auto-rematch system, or dedicated facility UI. The baseline heuristic AI may not handle doubles or Balanced Hackmons effectively. Only two sample opponent rosters are provided per category; sample teams still need server-side legality verification. No OpenAI API is required for the bot.
