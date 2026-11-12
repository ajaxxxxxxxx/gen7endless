# Gen7Endless — Gen 7 Battle Facility (prototype)

Local single-player Battle Maison/Tree-inspired Pokémon Showdown facility. **The custom Hackmons format is now explicitly official-style:** conventional 510 total EVs (252 per stat), legitimate 0–31 IVs, level 50, Mega Evolution only during battle with the appropriate Mega Stone, Species Clause, Item Clause, and prohibited restricted/box legendary and Mythical species. Moves and abilities may be reassigned under the original Gen 7 Balanced Hackmons bans.

### Formats

- `bh4`: six entrants, select four, doubles; `bh6`: six used, doubles.
- `lc3`: six entrants, select three, singles; `lc6`: six used, singles. Level 5 and historical Little Cup rules plus Item Clause.

### What counts as a legendary?

We use the Showdown **Restricted Legendary** and **Mythical** species categories, not a blanket ban on all legendary Pokémon. Ordinary legendaries such as the legendary birds, beasts, and many others can remain available subject to the validator; box and event special Pokémon cannot appear in the player's or the AI's teams. The 30/40 milestone is renamed **ace** rather than legendary: legal powerful Pokémon may appear, not banned box legendaries.

### Progression

1–50: mostly competent mixed rosters; 10/20 tough; 15/25/35/45 coordinated themes; 30/40 ace encounters; 50 OU-style team. 51+: non-checkpoint weights 30% regular, 25% tough, 15% themed, 10% ace, 20% optimized. Every fifth battle from 55 is optimized Hackmons (or themed Little Cup). AI and player use the same server-side validator.

### Setup

1. Clone official [Pokémon Showdown](https://github.com/smogon/pokemon-showdown) and this repository. Install Node.js and Python.
2. Run `python scripts/install_showdown.py /path/to/pokemon-showdown`; build the official server following its documentation.
3. Install `python -m pip install -r requirements.txt`; test with `python -m unittest discover -s tests`.
4. Run `python -m facility.bot --format bh4 --human YOUR_SHOWDOWN_USERNAME` and connect a locally hosted Showdown client.
5. Run `scripts/verify_formats.cjs` and `scripts/verify_teams.cjs` inside a built Showdown checkout to check the resulting formats and example rosters.

**Development limitations:** No packaged browser client or automatic next-match UI. The example opponent teams are illustrative and haven't passed a live Showdown validator check; additional balancing is needed. The poke-env integration and custom format compilation are also not yet verified end to end.
