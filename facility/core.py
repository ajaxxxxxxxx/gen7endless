"""Dependency-free facility state and candidate selection logic."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import random

FORMATS = {
    "bh4": ("gen7ajbhdoubles4", "bh"),
    "bh6": ("gen7ajbhdoubles6", "bh"),
    "lc3": ("gen7ajlcsingles3", "lc"),
    "lc6": ("gen7ajlcsingles6", "lc"),
}


def load_teams(team_dir: Path, category: str) -> list[tuple[str, str]]:
    folder = team_dir / category
    results = []
    for file in sorted(folder.glob('*.txt')):
        raw = file.read_text(encoding='utf-8').strip()
        if len([section for section in raw.split('\n\n') if section.strip()]) != 6:
            raise ValueError(f"{file}: expected exactly six Pokemon sets")
        results.append((file.name, raw))
    if not results:
        raise ValueError(f'No teams in {folder}')
    return results


class StreakStore:
    def __init__(self, path: Path):
        self.path = path
        self.state = {"version": 1, "formats": {}, "history": []}
        if path.exists():
            self.state = json.loads(path.read_text(encoding='utf-8'))

    def record(self, format_key: str, player_won: bool | None, opponent_team: str, battle_tag: str) -> dict:
        data = self.state['formats'].setdefault(format_key, {"current": 0, "best": 0, "wins": 0, "losses": 0, "ties": 0})
        if player_won is True:
            data['current'] += 1
            data['wins'] += 1
            data['best'] = max(data['best'], data['current'])
        elif player_won is False:
            data['current'] = 0
            data['losses'] += 1
        else:
            data['ties'] += 1
        self.state['history'].append({"when": datetime.now(timezone.utc).isoformat(), "format": format_key,
            "player_won": player_won, "opponent_team": opponent_team, "battle_tag": battle_tag})
        self.state['history'] = self.state['history'][-1000:]
        self._save()
        return data.copy()

    def current(self, format_key: str) -> int:
        return self.state['formats'].get(format_key, {}).get('current', 0)

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + '.tmp')
        temp.write_text(json.dumps(self.state, indent=2), encoding='utf-8')
        os.replace(temp, self.path)


def select_team(teams: list[tuple[str, str]], streak: int, rng: random.Random | None = None) -> tuple[str, str]:
    # All sets are format-legal, including early and late battle sets.
    # Rotate within a selected roster; do NOT provide banned powers to either side.
    rng = rng or random.Random()
    return rng.choice(teams)
