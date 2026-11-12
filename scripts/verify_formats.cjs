// Run from the official showdown repository ROOT after npm run build.
// This checks all four formats and exact preview/active-team size rules.
const {Dex} = require('./dist/sim/dex');
const tests = [
  ['gen7ajbhdoubles4', 'doubles', 4],
  ['gen7ajbhdoubles6', 'doubles', 6],
  ['gen7ajlcsingles3', 'singles', 3],
  ['gen7ajlcsingles6', 'singles', 6],
];
let failures = 0;
for (const [id, gameType, selected] of tests) {
  try {
    const f = Dex.formats.get(id);
    if (!f.exists) throw Error('not registered');
    const rules = Dex.formats.getRuleTable(f);
    if (f.gameType !== gameType || rules.pickedTeamSize !== selected || rules.maxTeamSize !== 6 || rules.minTeamSize !== 6) {
      throw Error(`unexpected settings: ${f.gameType} / ${rules.pickedTeamSize} / ${rules.minTeamSize} / ${rules.maxTeamSize}`);
    }
    console.log(`PASS ${id}: ${gameType}, bring six, select ${selected}`);
  } catch (e) { failures++; console.error(`FAIL ${id}: ${e.message}`); }
}
process.exitCode = failures ? 1 : 0;
