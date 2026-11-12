# NPC-only restricted legendary benchmarks

## Design intent

The Battle Spot-style player format remains restricted: no Restricted Legendary or Mythical species. The **NPC facility controller** may occasionally field those species at fixed benchmark encounters, initially battles 30 and 40. The stronger Pokémon should have eccentric, often significantly suboptimal moves/EVs/items, making them memorable rather than reliably brutal.

The user-provided examples are included in `benchmarks.json` as **design candidates**, not yet legal teams. Each benchmark team should contain just one featured restricted species unless explicitly authored otherwise. Other five team slots use the ordinary species roster, with Species Clause and Item Clause.

## Implementation gate

A Showdown format is normally symmetrical: the current `Restricted Legendary` and `Mythical` bans validate both users. Simply making the NPC team available in `teams/bh/` would cause rejected team submissions. For this reason, `benchmarks.json` is not loaded by `facility/core.py`, and the currently functional `ace` pool remains in use at 30/40.

Before enabling these encounters, add a **trusted server-side battle creation path** that distinguishes the NPC account from the human; validate the human against the normal `bh4` / `bh6` restrictions and the NPC against an alternative ruleset that relaxes **only the restricted species ban**, retaining the Gen 7 Balanced Hackmons restrictions, Species Clause, Item Clause, conventional stats, and Mega Evolution rules. The server must enforce that only the configured local NPC identity can access this exception. An ordinary client-supplied user name is insufficient authorization.

Never implement this by removing the species ban from the shared format, and never make the exception an option available to arbitrary battle participants.

## Pacing

- Battles 10/20: strong normal trainers.
- 15/25/35/45: coordinated archetypes.
- 30/40: planned exceptional trainer with a deliberately nonoptimized restricted species.
- 50: ordinary competitive OU-style team.
- 55 and every fifth onward: optimized Hackmons checkpoint, with normal battles between them.
- No randomly injected restricted species outside dedicated benchmarks unless separately approved.

## Balance and testing

Measure actual performance, not just species BST. Opponents using setup without reliable damage can produce lengthy, noninteractive turns; test for stalled matches and add a turn-based decision safeguard. Every bench team needs a legality test using the NPC validator, plus a negative test proving the same team is rejected by the player's validator. Confirm conventional EV caps, unique species/items, forms, and no illegal abilities/moves in both paths.
