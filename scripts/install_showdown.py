"""Copy the custom format definition into an already cloned Showdown checkout."""
import argparse
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('showdown_dir', type=Path)
args = parser.parse_args()
target = args.showdown_dir.resolve() / 'config' / 'custom-formats.ts'
if not (target.parent.parent / 'package.json').exists():
    raise SystemExit('Not a Pokemon Showdown checkout: missing package.json')
if target.exists():
    raise SystemExit(f'{target} already exists. Move it before installing (not overwritten).')
shutil.copy2(root / 'showdown-config' / 'custom-formats.ts', target)
print(f'Installed: {target}')
print('Now run `npm install`, `npm run build`, then `node pokemon-showdown start --no-security` from the Showdown directory.')
