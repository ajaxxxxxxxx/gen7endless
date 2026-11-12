import tempfile
import unittest
from pathlib import Path
from facility.core import FORMATS, StreakStore, load_teams

class CoreTests(unittest.TestCase):
    def test_four_formats(self):
        self.assertEqual(set(FORMATS), {'bh4','bh6','lc3','lc6'})
    def test_team_rosters(self):
        root = Path(__file__).resolve().parents[1] / 'teams'
        for category in ('bh','lc'):
            self.assertGreaterEqual(len(load_teams(root, category)), 2)
    def test_streak_persists_and_resets(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'record.json'
            s = StreakStore(path)
            s.record('bh4', True, 'a', 'b1')
            s.record('bh4', True, 'a', 'b2')
            self.assertEqual(StreakStore(path).current('bh4'), 2)
            s.record('bh4', False, 'b', 'b3')
            self.assertEqual(StreakStore(path).current('bh4'), 0)
            self.assertEqual(StreakStore(path).state['formats']['bh4']['best'], 2)
            self.assertEqual(len(StreakStore(path).state['history']), 3)
    def test_ties_keep_streak(self):
        with tempfile.TemporaryDirectory() as d:
            s = StreakStore(Path(d) / 'record.json')
            s.record('lc3', True, 'a', 'b1')
            s.record('lc3', None, 'a', 'b2')
            self.assertEqual(s.current('lc3'), 1)

if __name__ == '__main__': unittest.main()
