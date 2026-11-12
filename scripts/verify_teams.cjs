// Copy into Showdown repo root after compilation; run node verify_teams.cjs <facility path>
const {Dex} = require('./dist/sim/dex');
const {TeamValidator} = require('./dist/sim/team-validator');
const {Teams} = require('./dist/sim/teams');
const fs = require('fs');
const path = require('path');
const facility = path.resolve(process.argv[2] || '.');
const directories = [
  ['bh','gen7ajbhdoubles4'], ['bh','gen7ajbhdoubles6'],
  ['lc','gen7ajlcsingles3'], ['lc','gen7ajlcsingles6']
];
let failures = 0;
for (const [folder, format] of directories) {
  const validator = TeamValidator.get(format);
  for (const name of fs.readdirSync(path.join(facility,'teams',folder)).filter(n=>n.endsWith('.txt'))) {
    try {
      const sets = Teams.import(fs.readFileSync(path.join(facility,'teams',folder,name),'utf8'));
      const errors = validator.validateTeam(Teams.pack(sets));
      if (errors) throw Error(errors.join('; '));
      console.log(`PASS ${format}: ${name}`);
    } catch (e) { failures++; console.error(`FAIL ${format}: ${name}: ${e.message}`); }
  }
}
process.exitCode = failures ? 1 : 0;
