"""Human-vs-bot streak service, using the existing local Showdown UI.

Run one process per format; challenge 'MaisonAI' from your own local client.
The bot waits for one battle at a time, records the outcome, and rotates
its team. No network access besides the local Showdown websocket is needed.
"""
import argparse
import asyncio
from pathlib import Path
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.baselines import SimpleHeuristicsPlayer
from .core import FORMATS, StreakStore, load_teams, select_team


class FacilityBot(SimpleHeuristicsPlayer):
    def __init__(self, *, store, format_key, opponent_team, **kwargs):
        self.store = store
        self.format_key = format_key
        self.opponent_team_name = opponent_team
        super().__init__(**kwargs)

    def choose_move(self, battle):
        try:
            return super().choose_move(battle)
        except (AttributeError, ValueError, IndexError, TypeError, KeyError):
            # In particular: doubles sets may have unusual Hackmons moves.
            return self.choose_random_move(battle)

    def _battle_finished_callback(self, battle):
        # `won` refers to the AI player, not the human player.
        human_won = None if battle.won is None else not battle.won
        data = self.store.record(self.format_key, human_won, self.opponent_team_name, battle.battle_tag)
        print(f'Finished {battle.battle_tag} | Human won: {human_won} | '
              f'Streak {data["current"]}, best {data["best"]}', flush=True)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=FORMATS, default='bh4')
    parser.add_argument('--human', required=True, help='Exact Showdown display name; only this player can challenge the bot')
    parser.add_argument('--bot-name', default='MaisonAI')
    parser.add_argument('--teams', type=Path, default=Path(__file__).resolve().parents[1] / 'teams')
    parser.add_argument('--save', type=Path, default=Path(__file__).resolve().parents[1] / 'saves' / 'streaks.json')
    args = parser.parse_args()
    format_id, category = FORMATS[args.format]
    teams = load_teams(args.teams, category)
    store = StreakStore(args.save)
    first_name, first_text = select_team(teams, store.current(args.format))
    bot = FacilityBot(
        account_configuration=AccountConfiguration(args.bot_name, None),
        server_configuration=LocalhostServerConfiguration,
        battle_format=format_id, team=first_text,
        max_concurrent_battles=1, start_timer_on_battle_start=False,
        store=store, format_key=args.format, opponent_team=first_name,
    )
    print(f'Local AI ready: {args.bot_name} | {format_id} | allowed human: {args.human}', flush=True)
    print('In the Showdown client: Find a user > MaisonAI > Challenge > choose this format.', flush=True)
    while True:
        await bot.accept_challenges(args.human, 1)
        name, text = select_team(teams, store.current(args.format))
        bot.opponent_team_name = name
        bot.update_team(text)


if __name__ == '__main__':
    asyncio.run(main())
