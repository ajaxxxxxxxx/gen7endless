# Gen 7 Endless — single-player Battle Facility (prototype)

A private Showdown-based Gen 7 Battle Maison / Battle Tree-style challenge. Four formats: Balanced Hackmons Doubles (bring 6/select 4 or use 6) and Little Cup Singles (bring 6/select 3 or use 6).

## Encounter pacing

The opponent schedule is intentionally **not** a constant competitive ladder:

| Battle | Encounter |
| --- | --- |
| 1–9 | Mostly uncoordinated, competent rosters |
| 10, 20 | Tough roster |
| 15, 25, 35, 45 | Coordinated theme (e.g., weather, Trick Room, hazards) |
| 30, 40 | Featured box-legendary roster in Hackmons; tougher ordinary LC opponent |
| 50 | OU-style conventional competitive team in Hackmons; tough LC opponent |
| 51 onward | Regular battles are a weighted mix of rosters, with optimized Hackmons encounters becoming common |
| Every fifth battle from 55 | Fixed challenge: optimized Hackmons team or themed LC team |

During 1–50, **no optimized Hackmons** roster enters the random pool. The ordinary challenge gradually weights toward the tough pool, but still regularly gives easier matchups. From 51 onward: Hackmons 30% regular, 25% tough, 15% theme, 10% legendary, 20% optimized outside checkpoints. All user/AI teams are subject to the same Showdown validator; level 50 for Hackmons and level 5 for LC.

The Gen 7 Little Cup pool substitutes strong Little Cup teams for legendary/OU landmarks. Starter rosters are **illustrative** and limited; expand them before considering the encounters diverse or historically faithful. The two optimized sample Hackmons teams are reused for the special legendary encounters for now.

## Setup

1. Install Node.js and Python. Clone official [Pokemon Showdown](https://github.com/smogon/pokemon-showdown) and this repository.
2. Run `python scripts/install_showdown.py /path/to/pokemon-showdown` from this repository. It will not overwrite an existing custom formats file.
3. Follow upstream Showdown setup/build instructions, configure localhost-only network access, and start the Showdown server. Do not expose a server launched with development security settings to the internet.
4. Run `python -m pip install -r requirements.txt` and `python -m unittest discover -s tests`.
5. Run `python -m facility.bot --format bh4 --human YOUR_SHOWDOWN_USERNAME`.
6. Connect a locally hosted Showdown client and manually challenge `MaisonAI`.

The prototype does **not** yet bundle a standalone browser interface, auto-rematches, or full NPC facility presentation. poke-env integration and custom format/team legality have **not** been verified end-to-end against a locally built Showdown; run `scripts/verify_formats.cjs` and `scripts/verify_teams.cjs` in the Showdown checkout as documented in those files. Doubles AI still needs substantial work; source includes baseline heuristic fallback.

Current progression code: `facility/progression.py`; roster categories: `facility/core.py`; sample teams: `teams/`. Streaks persist to `saves/streaks.json` and are separate per format.
