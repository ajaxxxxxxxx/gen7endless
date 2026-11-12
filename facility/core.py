"""Team pool selection and persistent facility records."""
from pathlib import Path
from datetime import datetime, timezone
import json
import random
import os
from .progression import plan_encounter

FORMATS = {
 "bh4":("gen7ajbhdoubles4","bh"),"bh6":("gen7ajbhdoubles6","bh"),
 "lc3":("gen7ajlcsingles3","lc"),"lc6":("gen7ajlcsingles6","lc")
}
POOLS = {
 "bh":{"regular":["regular-01.txt"],"tough":["tough-01.txt"],
       "theme":["theme-01.txt"],"legendary":["01-tailwind.txt","02-trick-room.txt"],
       "ou":["ou-01.txt"],"optimized":["01-tailwind.txt","02-trick-room.txt"]},
 "lc":{"regular":["01-balance.txt"],"tough":["02-offense.txt"],
       "theme":["01-balance.txt","02-offense.txt"]}
}

def load_teams(team_dir:Path, category:str):
    rosters={}
    for tier, names in POOLS[category].items():
        pool=[]
        for name in names:
            content=(team_dir/category/name).read_text(encoding="utf8").strip()
            if len([x for x in content.split("\n\n") if x.strip()]) != 6:
                raise ValueError(f"{category}/{name} must contain six sets")
            pool.append((name,content))
        rosters[tier]=pool
    return rosters

def select_team(rosters, streak, format_key, rng=None):
    rng=rng or random.Random()
    encounter=plan_encounter(streak+1,format_key,rng)
    if encounter.pool not in rosters or not rosters[encounter.pool]:
        raise ValueError(f"Missing roster pool {encounter.pool}")
    name, content=rng.choice(rosters[encounter.pool])
    return name,content,encounter.pool

class StreakStore:
    def __init__(self,path:Path):
        self.path=path
        self.state={"version":1,"formats":{},"history":[]}
        if path.exists(): self.state=json.loads(path.read_text(encoding="utf8"))
    def current(self,key):
        return self.state["formats"].get(key,{}).get("current",0)
    def record(self,key,won,opponent_team,battle_tag,encounter_pool=None):
        d=self.state["formats"].setdefault(key,{"current":0,"best":0,"wins":0,"losses":0,"ties":0})
        if won is True:
            d["current"]+=1;d["wins"]+=1;d["best"]=max(d["best"],d["current"])
        elif won is False:
            d["current"]=0;d["losses"]+=1
        else:d["ties"]+=1
        self.state["history"].append({"when":datetime.now(timezone.utc).isoformat(),
          "format":key,"player_won":won,"opponent_team":opponent_team,
          "battle_tag":battle_tag,"encounter_pool":encounter_pool})
        self.state["history"]=self.state["history"][-1000:]
        self.path.parent.mkdir(parents=True,exist_ok=True)
        tmp=self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state,indent=2),encoding="utf8")
        os.replace(tmp,self.path)
        return d.copy()
