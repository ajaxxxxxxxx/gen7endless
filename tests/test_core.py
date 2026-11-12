import random
import tempfile
import unittest
from pathlib import Path
from facility.core import FORMATS, StreakStore, load_teams, select_team
from facility.progression import plan_encounter

class ProgressionTests(unittest.TestCase):
 def test_formats(self):
  self.assertEqual(set(FORMATS),{"bh4","bh6","lc3","lc6"})
 def test_milestones(self):
  expected={10:"tough",15:"theme",20:"tough",25:"theme",30:"legendary",
            35:"theme",40:"legendary",45:"theme",50:"ou",55:"optimized",60:"optimized"}
  for n,tier in expected.items():
   self.assertEqual(plan_encounter(n,"bh4").pool,tier)
   self.assertTrue(plan_encounter(n,"bh4").checkpoint)
  for n in (30,40,50,55):
   self.assertNotIn(plan_encounter(n,"lc3").pool,("legendary","ou","optimized"))
 def test_no_early_optimized(self):
  rng=random.Random(45)
  for n in range(1,51):
   for _ in range(30):
    tier=plan_encounter(n,"bh6",rng).pool
    self.assertNotEqual(tier,"optimized")
    if n not in (30,40): self.assertNotEqual(tier,"legendary")
 def test_rosters_and_selection(self):
  base=Path(__file__).resolve().parents[1]/"teams"
  for cat in ("bh","lc"): self.assertTrue(load_teams(base,cat))
  teams=load_teams(base,"bh")
  for n,tier in ((10,"tough"),(15,"theme"),(30,"legendary"),(50,"ou"),(55,"optimized")):
   name,content,selected=select_team(teams,n-1,"bh4",random.Random(1))
   self.assertEqual(selected,tier)
   self.assertTrue(name and content)
 def test_streaks(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/"save.json";s=StreakStore(path)
   s.record("bh4",True,"a","b1","regular")
   s.record("bh4",True,"a","b2","tough")
   s.record("bh4",None,"a","b3","regular")
   self.assertEqual(StreakStore(path).current("bh4"),2)
   s.record("bh4",False,"a","b4","regular")
   self.assertEqual(StreakStore(path).current("bh4"),0)
   self.assertEqual(StreakStore(path).state["formats"]["bh4"]["best"],2)
if __name__=="__main__":unittest.main()
