"""Maison-style progression. No restricted legendaries at any checkpoint."""
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Encounter:
    number: int
    pool: str
    checkpoint: bool=False

def plan_encounter(number:int,format_key:str,rng=None)->Encounter:
    if number<1: raise ValueError("number must be positive")
    if format_key not in ("bh4","bh6","lc3","lc6"): raise ValueError("unknown format")
    rng=rng or random.Random()
    bh=format_key.startswith("bh")
    if number<=50:
        milestones={10:"tough",15:"theme",20:"tough",25:"theme",
                    30:"ace" if bh else "tough",35:"theme",
                    40:"ace" if bh else "tough",45:"theme",
                    50:"ou" if bh else "tough"}
        if number in milestones: return Encounter(number,milestones[number],True)
        pools=([("regular",.90),("tough",.10)] if number<=10 else
               [("regular",.75),("tough",.25)] if number<=25 else
               [("regular",.60),("tough",.40)])
    else:
        if number%5==0: return Encounter(number,"optimized" if bh else "theme",True)
        pools=([("regular",.30),("tough",.25),("theme",.15),("ace",.10),("optimized",.20)] if bh
               else [("regular",.40),("tough",.30),("theme",.30)])
    roll=rng.random()
    for pool,weight in pools:
        roll-=weight
        if roll<0: return Encounter(number,pool)
    return Encounter(number,pools[-1][0])
