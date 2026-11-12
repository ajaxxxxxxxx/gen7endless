/** Gen7Endless: official-style roster legality + Hackmons move/ability freedom. */
export const Formats: import('../sim/dex-formats').FormatList = [
  {section: 'AJ Singleplayer Battle Facility', column: 4},
  {
    name: '[Gen 7] AJ BH Doubles 4', mod: 'gen7', gameType: 'doubles', searchShow: false, rated: false,
    ruleset: ['[Gen 7] Balanced Hackmons', 'Obtainable Formes', 'Obtainable Misc', 'Species Clause', 'Item Clause',
      'Min Team Size = 6', 'Max Team Size = 6', 'Picked Team Size = 4', 'Adjust Level = 50'],
    banlist: ['Restricted Legendary', 'Mythical'],
  },
  {
    name: '[Gen 7] AJ BH Doubles 6', mod: 'gen7', gameType: 'doubles', searchShow: false, rated: false,
    ruleset: ['[Gen 7] Balanced Hackmons', 'Obtainable Formes', 'Obtainable Misc', 'Species Clause', 'Item Clause',
      'Min Team Size = 6', 'Max Team Size = 6', 'Picked Team Size = 6', 'Adjust Level = 50'],
    banlist: ['Restricted Legendary', 'Mythical'],
  },
  {
    name: '[Gen 7] AJ LC Singles 3', mod: 'gen7', gameType: 'singles', searchShow: false, rated: false,
    ruleset: ['[Gen 7] LC', 'Item Clause', 'Min Team Size = 6', 'Max Team Size = 6', 'Picked Team Size = 3', 'Max Level = 5'],
  },
  {
    name: '[Gen 7] AJ LC Singles 6', mod: 'gen7', gameType: 'singles', searchShow: false, rated: false,
    ruleset: ['[Gen 7] LC', 'Item Clause', 'Min Team Size = 6', 'Max Team Size = 6', 'Picked Team Size = 6', 'Max Level = 5'],
  },
];
