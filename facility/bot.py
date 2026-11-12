"""Local battle bot. Integration with upstream poke-env remains experimental."""
import argparse
import asyncio
from pathlib import Path
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from poke_env.player.baselines import SimpleHeuristicsPlayer
from .core import FORMATS, StreakStore, load_teams, select_team

class FacilityBot(SimpleHeuristicsPlayer):
    def __init__(self,*,store,format_key,opponent_team,encounter_pool,**kwargs):
        self.store=store
        self.format_key=format_key
        self.opponent_team_name=opponent_team
        self.encounter_pool=encounter_pool
        super().__init__(**kwargs)
    def choose_move(self,battle):
        try:return super().choose_move(battle)
        except (AttributeError,ValueError,IndexError,TypeError,KeyError):
            return self.choose_random_move(battle)
    def _battle_finished_callback(self,battle):
        human_won=None if battle.won is None else not battle.won
        data=self.store.record(self.format_key,human_won,self.opponent_team_name,
                               battle.battle_tag,self.encounter_pool)
        print(f'Finished {battle.battle_tag} | Human win: {human_won} | '
              f'Streak {data["current"]}, best {data["best"]}',flush=True)

async def main():
    p=argparse.ArgumentParser()
    p.add_argument("--format",choices=FORMATS,default="bh4")
    p.add_argument("--human",required=True)
    p.add_argument("--bot-name",default="MaisonAI")
    p.add_argument("--teams",type=Path,default=Path(__file__).resolve().parents[1]/"teams")
    p.add_argument("--save",type=Path,default=Path(__file__).resolve().parents[1]/"saves"/"streaks.json")
    a=p.parse_args()
    fmt,category=FORMATS[a.format]
    rosters=load_teams(a.teams,category)
    store=StreakStore(a.save)
    name,content,pool=select_team(rosters,store.current(a.format),a.format)
    bot=FacilityBot(account_configuration=AccountConfiguration(a.bot_name,None),
        server_configuration=LocalhostServerConfiguration,battle_format=fmt,
        team=content,max_concurrent_battles=1,start_timer_on_battle_start=False,
        store=store,format_key=a.format,opponent_team=name,encounter_pool=pool)
    print(f'Waiting for {a.human} on {fmt}',flush=True)
    while True:
        await bot.accept_challenges(a.human,1)
        name,content,pool=select_team(rosters,store.current(a.format),a.format)
        bot.opponent_team_name=name
        bot.encounter_pool=pool
        bot.update_team(content)
if __name__=="__main__":asyncio.run(main())
