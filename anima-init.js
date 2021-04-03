const AnimaInitiative = (() => {
  // eslint-disable-line no-unused-vars
  log('DEBUG 0: script loaded');

  const scriptName = 'AnimaInitiative';
  const version = '0.0.1';

  const isString = (s) => 'string' === typeof s || s instanceof String;
  const isFunction = (f) => 'function' === typeof f;

  const DefaultCharacterFumble = 3;
  const DefaultCharacterOpenRoll = 90;

  const ColorRed = '#B31515';
  const ColorGreen = '#3FB315';
  const ColorBlue = '#4A57ED';
  const ColorYellow = '#FFD800';
  const ColorWhite = 'white';

  let observers = {
    turnOrderChange: [],
  };

  const sorters = {
    None: {
      desc: `No sorting is applied.`,
      func: (to) => to,
    },
    Ascending: {
      desc: `Sorts the Turn Order from highest to lowest`,
      func: (to, preserveFirst) => {
        let first = to[0];
        const sorter_asc = (a, b) => a.pr - b.pr;
        let newTo = to.sort(sorter_asc);
        if (preserveFirst) {
          let idx = newTo.findIndex((e) => e === first);
          newTo = [...newTo.slice(idx), ...newTo.slice(0, idx)];
        }
        return newTo;
      },
    },
    Descending: {
      desc: `Sorts the Turn Order from lowest to highest.`,
      func: (to, preserveFirst) => {
        let first = to[0];
        const sorter_desc = (a, b) => b.pr - a.pr;
        let newTo = to.sort(sorter_desc);
        if (preserveFirst) {
          let idx = newTo.findIndex((e) => e === first);
          newTo = [...newTo.slice(idx), ...newTo.slice(0, idx)];
        }
        return newTo;
      },
    },
  };

  const ch = (c) => {
    const entities = {
      '<': 'lt',
      '>': 'gt',
      '&': 'amp',
      "'": '#39',
      '@': '#64',
      '{': '#123',
      '|': '#124',
      '}': '#125',
      '[': '#91',
      ']': '#93',
      '"': 'quot',
      '*': 'ast',
      '/': 'sol',
      ' ': 'nbsp',
    };

    if (entities.hasOwnProperty(c)) {
      return `&${entities[c]};`;
    }
    return '';
  };

  const HE = (() => {
    const esRE = (s) => s.replace(/(\\|\/|\[|\]|\(|\)|\{|\}|\?|\+|\*|\||\.|\^|\$)/g, '\\$1');
    const e = (s) => `&${s};`;
    const entities = {
      '<': e('lt'),
      '>': e('gt'),
      "'": e('#39'),
      '@': e('#64'),
      '{': e('#123'),
      '|': e('#124'),
      '}': e('#125'),
      '[': e('#91'),
      ']': e('#93'),
      '"': e('quot'),
    };
    const re = new RegExp(`(${Object.keys(entities).map(esRE).join('|')})`, 'g');
    return (s) => s.replace(re, (c) => entities[c] || c);
  })();
  
  const _h = {
    outer: (...o) =>
      `<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">${o.join(' ')}</div>`,
    title: (t, v) => `<div style="font-weight: bold; border-bottom: 1px solid black;font-size: 130%;">${t} v${v}</div>`,
    subhead: (...o) => `<b>${o.join(' ')}</b>`,
    minorhead: (...o) => `<u>${o.join(' ')}</u>`,
    optional: (...o) => `${ch('[')}${o.join(` ${ch('|')} `)}${ch(']')}`,
    required: (...o) => `${ch('<')}${o.join(` ${ch('|')} `)}${ch('>')}`,
    header: (...o) => `<div style="padding-left:10px;margin-bottom:3px;">${o.join(' ')}</div>`,
    section: (s, ...o) => `${_h.subhead(s)}${_h.inset(...o)}`,
    paragraph: (...o) => `<p>${o.join(' ')}</p>`,
    items: (o) => o.map((i) => `<li>${i}</li>`).join(''),
    ol: (...o) => `<ol>${_h.items(o)}</ol>`,
    ul: (...o) => `<ul>${_h.items(o)}</ul>`,
    grid: (...o) => `<div style="padding: 12px 0;">${o.join('')}<div style="clear:both;"></div></div>`,
    cell: (o) => `<div style="width: 130px; padding: 0 3px; float: left;">${o}</div>`,
    inset: (...o) => `<div style="padding-left: 10px;padding-right:20px">${o.join(' ')}</div>`,
    join: (...o) => o.join(' '),
    pre: (...o) =>
      `<div style="border:1px solid #e1e1e8;border-radius:4px;padding:8.5px;margin-bottom:9px;font-size:12px;white-space:normal;word-break:normal;word-wrap:normal;background-color:#f7f7f9;font-family:monospace;overflow:auto;">${o.join(
        ' '
      )}</div>`,
    preformatted: (...o) => _h.pre(o.join('<br>').replace(/\s/g, ch(' '))),
    code: (...o) => `<code>${o.join(' ')}</code>`,
    attr: {
      bare: (o) => `${ch('@')}${ch('{')}${o}${ch('}')}`,
      selected: (o) => `${ch('@')}${ch('{')}selected${ch('|')}${o}${ch('}')}`,
      target: (o) => `${ch('@')}${ch('{')}target${ch('|')}${o}${ch('}')}`,
      char: (o, c) => `${ch('@')}${ch('{')}${c || 'CHARACTER NAME'}${ch('|')}${o}${ch('}')}`,
    },
    bold: (...o) => `<b>${o.join(' ')}</b>`,
    italic: (...o) => `<i>${o.join(' ')}</i>`,
    font: {
      command: (...o) => `<b><span style="font-family:serif;">${o.join(' ')}</span></b>`,
    },
    ui: {
      float: (t) => `<div style="display:inline-block;float:right">${t}</div>`,
      clear: () => `<div style="clear:both;"></div>`,
      bubble: (label) =>
        `<span style="display:inline-block;border:1px solid #999; border-radius: 1em; padding: .1em 1em; font-weight:bold; background-color: #009688;color:white">${label}</span>`,
      button: (label, link) => `<a href="${link}">${label}</a>`,
    },
  };
  
  const initScript = function () {
    initStat = [
      [
        {
          attribute: 'repeating_initiative_$0_init_final',
        },
      ],
    ];
    state[scriptName] = {
      lastHelpVersion: version,
      bonusStatGroups: initStat,
      savedTurnOrders: [],
      config: {
        rollType: 'Individual-Roll',
        replaceRoll: true,
        dieSize: 100,
        diceCount: 1,
        criticalSuccess: 90,
        criticalFailure: 3,
        characterFailAttribute: 'f_base',
        characterSuccessAttribute: 'or_base',
        maxDecimal: 2,
        autoOpenInit: true,
        sortOption: 'Descending',
        preserveFirst: false,
        announcer: 'Partial',
      },
    };
    createHelpHandout();
  };

  const observeTurnOrderChange = function (handler) {
    if (handler && _.isFunction(handler)) {
      observers.turnOrderChange.push(handler);
    }
  };

  const notifyObservers = function (event, obj, prev) {
    _.each(observers[event], function (handler) {
      handler(obj, prev);
    });
  };

  const formatDieRoll = function (rollData, character) {
    // The following can fail if the tokens are not properly hooked up to the character sheets.
    var characterFail = character
      ? parseInt(getAttrByName(character.id, state[scriptName].config.characterFailAttribute))
      : DefaultCharacterFumble;
    var characterSuccess = character
      ? parseInt(getAttrByName(character.id, state[scriptName].config.characterSuccessAttribute))
      : DefaultCharacterOpenRoll;
    var critFail = _.reduce(
      rollData.rolls,
      function (m, r) {
        return (
          m ||
          (characterFail && r.rolls.some((roll) => roll <= characterFail)) ||
          r.rolls.some((roll) => roll <= state[scriptName].config.criticalFailure)
        );
      },
      false
    );
    var critSuccess = _.reduce(
      rollData.rolls,
      function (m, r) {
        return (
          m ||
          (characterSuccess && r.rolls.some((roll) => roll >= characterSuccess)) ||
          r.rolls.some((roll) => roll >= state[scriptName].config.criticalSuccess)
        );
      },
      false
    );
    var highlight = critFail && critSuccess ? ColorBlue : critFail ? ColorRed : critSuccess ? ColorGreen : ColorYellow;
    var dicePart = _.reduce(
      rollData.rolls,
      function (m, r) {
        _.reduce(
          r.rolls,
          function (dm, dr) {
            var dielight = dr <= characterFail ? ColorRed : dr >= characterSuccess ? ColorGreen : ColorWhite;
            dm.push('<span style="font-weight:bold;color:' + dielight + ';">' + dr + '</span>');
            return dm;
          },
          m
        );
        return m;
      },
      []
    ).join(' + ');

    return (
      '<span class="inlinerollresult showtip tipsy" style="min-width:1em;display: inline-block; border: 2px solid ' +
      highlight +
      '; background-color: #FEF68E;color: #404040; font-weight:bold;padding: 0px 3px;cursor: help"' +
      ' title="' +
      HE(
        HE(
          '<span style="color:white;">' +
            dicePart +
            ' [init] ' +
            (rollData.bonus >= 0 ? '+' : '-') +
            ' <span style="font-weight:bold;">' +
            Math.abs(rollData.bonus) +
            '</span> [bonus]' +
            '</span>'
        )
      ) +
      '">' +
      rollData.total +
      '</span>'
    );
  };

  const buildAnnounceGroups = function (l) {
    var groupColors = {
      npc: '#eef',
      character: '#efe',
      gmlayer: '#aaa',
    };
    return _.reduce(
      l,
      function (m, s) {
        var type =
          'gmlayer' === s.token.get('layer')
            ? 'gmlayer'
            : (s.character &&
                _.filter(s.character.get('controlledby').split(/,/), function (c) {
                  return 'all' === c || ('' !== c && !playerIsGM(c));
                }).length > 0) ||
              false
            ? 'character'
            : 'npc';
        if ('graphic' !== s.token.get('type') || 'token' !== s.token.get('subtype')) {
          return m;
        }
        m[type].push(
          '<div style="float: left;display: inline-block;border: 1px solid #888;border-radius:5px; padding: 1px 3px;background-color:' +
            groupColors[type] +
            ';">' +
            '<div style="font-weight:bold; font-size: 1.3em;">' +
            '<img src="' +
            (s.token && s.token.get('imgsrc')) +
            '" style="height: 2.5em;float:left;margin-right:2px;">' +
            ((s.token && s.token.get('name')) || (s.character && s.character.get('name')) || '(Creature)') +
            '</div>' +
            '<div>' +
            formatDieRoll(s.rollResults, s.character) +
            '</div>' +
            '<div style="clear: both;"></div>' +
            '</div>'
        );
        return m;
      },
      { npc: [], character: [], gmlayer: [] }
    );
  };

  const announcers = {
    None: {
      desc: `Shows nothing in chat when a roll is made.`,
      func: () => {},
    },
    Hidden: {
      desc: `Whispers all rolls to the GM, regardless of who controls the tokens.`,
      func: (l) => {
        let groups = buildAnnounceGroups(l);
        if (groups.npc.length || groups.character.length || groups.gmlayer.length) {
          sendChat(
            scriptName,
            '/w gm ' +
              '<div>' +
              groups.character.join('') +
              groups.npc.join('') +
              groups.gmlayer.join('') +
              '<div style="clear:both;"></div>' +
              '</div>'
          );
        }
      },
    },
    Partial: {
      desc: `Character rolls are shown in chat (Player controlled tokens), all others are whispered to the GM.`,
      func: (l) => {
        let groups = buildAnnounceGroups(l);
        if (groups.character.length) {
          sendChat(
            scriptName,
            '/direct ' + '<div>' + groups.character.join('') + '<div style="clear:both;"></div>' + '</div>'
          );
        }
        if (groups.npc.length || groups.gmlayer.length) {
          sendChat(
            scriptName,
            '/w gm ' +
              '<div>' +
              groups.npc.join('') +
              groups.gmlayer.join('') +
              '<div style="clear:both;"></div>' +
              '</div>'
          );
        }
      },
    },
    Visible: {
      desc: `Rolls for tokens on the Objects Layer are shown to all in chat.  Tokens on the GM Layer have their rolls whispered to the GM. `,
      func: (l) => {
        let groups = buildAnnounceGroups(l);
        if (groups.npc.length || groups.character.length) {
          sendChat(
            scriptName,
            '/direct ' +
              '<div>' +
              groups.character.join('') +
              groups.npc.join('') +
              '<div style="clear:both;"></div>' +
              '</div>'
          );
        }
        if (groups.gmlayer.length) {
          sendChat(
            scriptName,
            '/w gm ' + '<div>' + groups.gmlayer.join('') + '<div style="clear:both;"></div>' + '</div>'
          );
        }
      },
    },
  };

  const buildInitDiceExpression = function (s) {
    return 'd100';
  };

  const createHelpHandout = () => {
    const helpIcon =
      'https://s3.amazonaws.com/files.d20.io/images/127392204/tAiDP73rpSKQobEYm5QZUw/thumb.png?15878425385';

    // find handout
    let props = { type: 'handout', name: `Help: ${scriptName}` };
    if (findObjs(props)[0]) {
      createObj('handout', Object.assign(props, { avatar: helpIcon }));
    }
  };

  const helpParts = {
    helpBody: (context) =>
      _h.join(
        _h.header(
          _h.paragraph(
            `Rolls initiative for the selected tokens and adds them to the Turn Order if they don${ch(
              "'"
            )}t have a turn yet.`
          ),
          _h.paragraph(
            `The calculation of initiative is handled by the combination of Roller (See ${_h.bold(
              'Roller Options'
            )} below) and a Bonus.  The Bonus is determined based on an ordered list of Stat Groups (See ${_h.bold(
              'Bonus Stat Groups'
            )} below).  Stat Groups are evaluated in order.  The bonus computed by the first Stat Group for which all attributes exist and have a numeric value is used.  This allows you to have several Stat Groups that apply to different types of characters.  In practice you will probably only have one, but more are there if you need them.`
          )
        ),
        helpParts.commands(context)
      ),
    rollingCommands: (/*context*/) =>
      _h.section(
        'Commands for Rolling',
        _h.paragraph(
          `AnimaInitiative's primary role is rolling initiative.  It has many options for performing the roll, most of which operate on the selected tokens.`
        ),
        _h.inset(
          _h.font.command(`!anima-init`),
          _h.paragraph(
            `This command uses the configured Roller to dtermine the initiative order for all the selected tokens.`
          ),
          _h.font.command(`!anima-init`, `--bonus`, _h.required('bonus')),
          _h.paragraph(
            `This command is just line the bare !anima-init roll, but will add the supplied bonus to all rolls.  The bonus can be from an inline roll.`
          ),
          _h.font.command(`!anima-init`, `--reroll`, _h.optional('bonus')),
          _h.paragraph(
            `This command rerolls all of the tokens currently in the turn order as if they were selected when you executed !anima-init.  An optional bonus can be supplied, which can be the result of an inline roll.`
          ),
          _h.font.command(`!anima-init`, `--ids`, _h.optional('...')),
          _h.paragraph(
            `This command uses the configured Roller to determine the initiative order for all tokens whose ids are specified.`
          ),

          _h.font.command(`!anima-init`, `--adjust`, _h.required('adjustment'), _h.optional('minimum')),
          _h.paragraph(
            `Applies an adjustment to all the current Turn Order tokens (Custom entries ignored).  The required adjustment value will be applied to the current value of all Turn Order entries.  The optional minium value will be used if the value after adjustiment is lower, which can end up raising Turn Order values even if they were already lower.`
          ),
          _h.font.command(`!anima-init`, `--adjust-current`, _h.required('adjustment'), _h.optional('minimum')),
          _h.paragraph(
            `This is identical to --adjust, save that it is only applied to the top entry in the Turn Order.`
          )
        )
      ),
    helpCommands: (/*context*/) =>
      _h.section(
        'Help and Configuration',
        _h.paragraph(
          `All of these commands are documented in the build in help.  Additionally, there are many configuration options that can only be accessed there.`
        ),
        _h.inset(
          _h.font.command(`!anima-init`, `--help`),
          _h.paragraph(`This command displays the help and configuration options.`)
        )
      ),

    stackCommands: (/*context*/) =>
      _h.section(
        'Commands for Stacks of Initiative',
        _h.paragraph(
          `AnimaInitiative provides a system called ${_h.bold(
            'Stacks'
          )} which lets you store collections of prerolled initiative values and combine or cycle them as desired.`
        ),
        _h.inset(
          _h.font.command(`!anima-init`, `--stack`, _h.optional('operation'), _h.optional('label')),
          _h.inset(
            _h.minorhead('Available Operations:'),
            _h.ul(
              `${_h.bold('list')} -- Displays the stack of saved Turn Orders. (default)`,
              `${_h.bold('clear')} -- Clears the stack of saved Turn Orders.`,
              `${_h.bold(
                `copy${ch('|')}dup ${ch('[')}label${ch(']')}`
              )} -- Adds a copy of the current Turn Order to the stack.`,
              `${_h.bold(
                `push ${ch('[')}label${ch(']')}`
              )} -- Adds a copy of the current Turn Order to the stack and clears the Turn Order.  Anything after the command will be used as a label for the entry.`,
              `${_h.bold(
                'pop'
              )} -- Replaces the current Turn Order with the last entry in the stack removing it from the stack.`,
              `${_h.bold(
                'apply'
              )} -- Replaces the current Turn Order with the last entry in the stack leaving it on the stack.`,
              `${_h.bold(
                `swap ${ch('[')}label${ch(']')}`
              )} -- Swaps the current Turn Order with the last entry in the stack.  Anything after the command will be used as a label for the entry placed in the stack.`,
              `${_h.bold(
                `tswap${ch('|')}tail-swap ${ch('[')}label${ch(']')}`
              )} -- Swaps the current Turn Order with the first entry in the stack.  Anything after the command will be used as a label for the entry placed in the stack.`,
              `${_h.bold(
                'merge'
              )} -- Removes the last entry in the stack and adds it to the current Turn Order and sorts the new Turn Order with the configured sort method.`,
              `${_h.bold(
                `apply-merge${ch('|')}amerge`
              )} -- Merges the last entry in the stack with the current Turn Order and sorts the new Turn Order with the configured sort method, leaving the stack unchanged.`,
              `${_h.bold(
                `rotate${ch('|')}rot ${ch('[')}label${ch(']')}`
              )} -- Pushes the current Turn Order onto the end of the stack and restores the first entry from the stack to the Turn Order.  Anything after the command will be used as a label for the entry placed in the stack.`,
              `${_h.bold(
                `reverse-rotate${ch('|')}rrot ${ch('[')}label${ch(']')}`
              )} -- Pushes the current Turn Order onto the beginning of the stack and restores the last entry from the stack to the Turn Order.  Anything after the command will be used as a label for the entry placed in the stack.`
            )
          )
        )
      ),
    turnOrderCommands: (/*context*/) =>
      _h.section(
        'Commands for Turn Order Management',
        _h.paragraph(
          `The Turn Order is an integral part of initiative, so AnimaInitiative provides soem methodes for manipulating it.`
        ),
        _h.inset(
          _h.font.command(`!anima-init`, `--toggle-turnorder`),
          _h.paragraph(`Opens or closes the Turn Order window.`),
          _h.font.command(`!anima-init`, `--sort`),
          _h.paragraph(`Applies the configured sort operation to the current Turn Order.`),
          _h.font.command(`!anima-init`, `--clear`),
          _h.paragraph(
            `Removes all tokens from the Turn Order.  If Auto Open Init is enabled it will also close the Turn Order box.`
          )
        )
      ),
    commands: (context) =>
      _h.join(
        _h.subhead('Commands'),
        helpParts.rollingCommands(context),
        helpParts.helpCommands(context),
        helpParts.turnOrderCommands(context),
        helpParts.stackCommands(context)
      ),

    sortOptionsConfig: (/* context */) =>
      _h.section(
        'Sorter Options',
        _h.paragraph(
          `The Sorter is used to determine how to reorder entries in the Turn Order whenever AnimaInitiative performs a sort.  Sorting occurs when the sort command (${_h.code(
            '!anima-init --sort'
          )}) is issued, when stack entries are merged into the current Turn Order, and when new entries are added to the Turn Order with a AnimaInitiative command (like ${_h.code(
            '!anima-init'
          )}).`
        ),
        _h.inset(
          _h.ul(
            ...Object.keys(sorters).map(
              (s) =>
                `${_h.ui.float(
                  s === state[scriptName].config.sortOption
                    ? _h.ui.bubble(_h.bold('Selected'))
                    : _h.ui.button(`Use ${s}`, `!anima-init-config --sort-option|${s}`)
                )}${_h.bold(s)} -- ${sorters[s].desc}${_h.ui.clear()}`
            )
          )
        )
      ),

    maxDecimalConfig: (/* context */) =>
      _h.section(
        'Maximum Decimal Places',
        _h.paragraph(
          `This is the Maximum number of decimal places to show in the Initiative when Tie-Breakers are rolled.`
        ),
        _h.inset(
          _h.paragraph(
            `${_h.ui.float(
              _h.ui.button(
                'Set Max Decimal',
                `!anima-init-config --set-max-decimal|?{Maximum number of decimal places:|${state[scriptName].config.maxDecimal}}`
              )
            )}Maximum Decimal Places is currently set to ${_h.bold(
              state[scriptName].config.maxDecimal
            )}. ${_h.ui.clear()}`
          )
        )
      ),
    autoOpenInitConfig: (/* context */) =>
      _h.section(
        'Auto Open Turn Order',
        _h.paragraph(`This option causes AnimaInitiative to open the Turn Order whenever it makes an initiative roll.`),
        _h.inset(
          _h.paragraph(
            `${_h.ui.float(
              _h.ui.button(
                state[scriptName].config.autoOpenInit ? 'Disable' : 'Enable',
                `!anima-init-config --toggle-auto-open-init`
              )
            )}Auto Open Turn Order is currently ${_h.bold(
              state[scriptName].config.autoOpenInit ? 'On' : 'Off'
            )}. ${_h.ui.clear()}`
          )
        )
      ),
    replaceRollConfig: (/* context */) =>
      _h.section(
        'Replace Roll',
        _h.paragraph(
          `This option causes AnimaInitiative to replace a roll in the Turn Order if a token is already present there when it makes a roll for it.  Otherwise, the token is ignored and the current roll is retained.`
        ),
        _h.inset(
          _h.paragraph(
            `${_h.ui.float(
              _h.ui.button(
                state[scriptName].config.replaceRoll ? 'Disable' : 'Enable',
                `!anima-init-config --toggle-replace-roll`
              )
            )}Replace Roll is currently ${_h.bold(
              state[scriptName].config.replaceRoll ? 'On' : 'Off'
            )}. ${_h.ui.clear()}`
          )
        )
      ),
    preserveFirstConfig: (/* context */) =>
      _h.section(
        'Preserve First on Sorted Add',
        _h.paragraph(
          `This option causes AnimaInitiative to preserve the first Turn Order entry when sorting the Turn Order after adding creatures.`
        ),
        _h.inset(
          _h.paragraph(
            `${_h.ui.float(
              _h.ui.button(
                state[scriptName].config.preserveFirst ? 'Disable' : 'Enable',
                `!anima-init-config --toggle-preserve-first`
              )
            )}Preserve First on Sorted Add is currently ${_h.bold(
              state[scriptName].config.preserveFirst ? 'On' : 'Off'
            )}. ${_h.ui.clear()}`
          )
        )
      ),
    announcerConfig: (/*context*/) =>
      _h.section(
        'Announcer Options',
        _h.paragraph(`The Announcer controls what is shown in chat when a roll is performed.`),
        _h.inset(
          _h.ul(
            ...Object.keys(announcers).map(
              (a) =>
                `${_h.ui.float(
                  a === state[scriptName].config.announcer
                    ? _h.ui.bubble(_h.bold('Selected'))
                    : _h.ui.button(`Use ${a}`, `!anima-init-config --set-announcer|${a}`)
                )}${_h.bold(a)} -- ${announcers[a].desc}${_h.ui.clear()}`
            )
          )
        )
      ),

    showBonusStatGroupsConfig: (/*context*/) =>
      _h.section(
        'Bonus Stat Groups',
        _h.inset(
          _h.ol(
            ...state[scriptName].bonusStatGroups.map(
              (a, n) =>
                `${_h.ui.float(_h.ui.button(`+`, `!anima-init --promote ${n + 1}`))}${_h.ui.float(
                  _h.ui.button(`X`, `!anima-init --del-group ${n + 1}`)
                )}${a
                  .map((e) =>
                    _h.ui.bubble(
                      (e.adjustments || []).reduce(
                        (m, adj) => `${adj}( ${m} )`,
                        `${e.attribute}|${e.type || 'current'}`
                      )
                    )
                  )
                  .join(' + ')}${_h.ui.clear()}`
            )
          )
        )
      ),

    configuration: (context) =>
      _h.join(
        _h.subhead('Configuration'),
        _h.inset(
          helpParts.sortOptionsConfig(context),
          helpParts.preserveFirstConfig(context),
          helpParts.maxDecimalConfig(context),
          helpParts.autoOpenInitConfig(context),
          helpParts.replaceRollConfig(context),
          helpParts.announcerConfig(context),
          helpParts.showBonusStatGroupsConfig(context)
        )
      ),

    helpConfig: (context) => _h.outer(_h.title(scriptName, version), helpParts.configuration(context)),

    helpDoc: (context) => _h.join(_h.title(scriptName, version), helpParts.helpBody(context)),

    helpChat: (context) =>
      _h.outer(_h.title(scriptName, version), helpParts.helpBody(context), helpParts.configuration(context)),
  };

  const showHelp = (playerid) => {
    const who = (getObj('player', playerid) || { get: () => 'API' }).get('_displayname');
    let context = {
      who,
      playerid,
    };
    sendChat('', '/w "' + who + '" ' + helpParts.helpChat(context));
  };

  const parseEmbeddedStatReferences = function (stat, charObj) {
    let charName = charObj.get('name'),
      stext = (stat + '')
        .replace(/@{[^}]*}/g, (s) => {
          let parts = _.rest(s.match(/@{([^|}]*)\|?([^|}]*)\|?([^|}]*)}/)),
            statName,
            modName;
          if (parts[2].length) {
            statName = parts[1];
            modName = parts[2];
          } else if (parts[1].length) {
            if (_.contains(['max', 'current'], parts[1])) {
              statName = parts[0];
              modName = parts[1];
            } else {
              statName = parts[1];
            }
          } else {
            statName = parts[0];
          }

          return `@{${charName}|${statName}${modName ? `|${modName}` : ''}}`;
        })
        .replace(/&{tracker}/, '');
    return stext;
  };

  const findInitiativeBonus = (charObj, token) => {
    let bonus = 0;
    state[scriptName].bonusStatGroups.find((group) => {
      bonus = group.map((details) => {
        let stat = getAttrByName(charObj.id, details.attribute, details.type || 'current');

        if (undefined === stat || null === stat) {
          stat = undefined;
        } else if (!Number.isNaN(Number(stat))) {
          stat = parseFloat(stat);
        } else if (isString(stat)) {
          stat = parseEmbeddedStatReferences(stat, charObj);
          stat = stat.length ? stat : 0;
        } else {
          stat = undefined;
        }

        return (details.adjustments || []).reduce((memo, a) => {
          return memo;
        }, stat);
      });

      if (_.contains(bonus, undefined) || _.contains(bonus, null) || _.contains(bonus, NaN)) {
        bonus = '';
        console.log('Could not find bonus!');
        return false;
      }
      bonus = bonus.join('+');
      return true;
    });
    return bonus;
  };

  const rollForTokenIDsExternal = (ids, options) => {
    if (Array.isArray(ids)) {
      setTimeout(
        () =>
          makeRollsForIDs(ids, {
            isReroll: false,
            prev: Campaign().get('turnorder'),
            manualBonus: parseFloat(options && options.manualBonus) || 0,
          }),
        0
      );
    }
  };

  const makeRollsForIDs = (ids, options = {}) => {
    let turnorder = Campaign().get('turnorder');

    turnorder = '' === turnorder ? [] : JSON.parse(turnorder);
    if (state[scriptName].config.replaceRoll || options.isReroll) {
      turnorder = turnorder.filter((e) => !ids.includes(e.id));
    }

    let turnorderIDS = turnorder.map((e) => e.id);

    let initFunc = () => 'd100';

    let rollSetup = ids
      .filter((id) => !turnorderIDS.includes(id))
      .map((id) => getObj('graphic', id))
      .filter((g) => undefined !== g)
      .map((g) => ({
        token: g,
        character: getObj('character', g.get('represents')),
      }))
      .map((g) => {
        g.roll = [];

        let bonus = findInitiativeBonus(g.character || {}, g.token);
        bonus = isString(bonus) ? (bonus.trim().length ? bonus : '0') : bonus;
        g.roll.push(bonus);

        if (options.manualBonus) {
          g.roll.push(options.manualBonus);
        }
        g.roll.push(initFunc(g));
        return g;
      });

    let pageid = (rollSetup[0] || { token: { get: () => {} } }).token.get('pageid');

    let initRolls = _.map(rollSetup, function (rs, i) {
      return {
        index: i,
        roll: (
          '[[(' +
          _.reject(rs.roll, function (r) {
            return _.isString(r) && _.isEmpty(r);
          }).join(') + (') +
          ')]]'
        ).replace(/\[\[\[/g, '[[ ['),
      };
    });

    let turnEntries = [];
    let finalize = _.after(initRolls.length, function () {
      turnEntries = _.sortBy(turnEntries, 'order');

      Campaign().set({
        turnorder: JSON.stringify(
          sorters[state[scriptName].config.sortOption].func(
            turnorder.concat(
              _.chain(rollSetup)
                .map(function (s) {
                  s.rollResults = turnEntries.shift();
                  return s;
                })
                .tap(announcers[state[scriptName].config.announcer].func)
                .map(function (s) {
                  return {
                    id: s.token.id,
                    pr: s.rollResults.total,
                    custom: '',
                  };
                })
                .value()
            ),
            state[scriptName].config.preserveFirst
          )
        ),
      });
      notifyObservers('turnOrderChange', Campaign().get('turnorder'), options.prev);

      if (state[scriptName].config.autoOpenInit && !Campaign().get('initativepage')) {
        Campaign().set({
          initiativepage: pageid,
        });
      }
    });

    _.each(initRolls, function (ir) {
      sendChat('', ir.index + ':' + ir.roll.replace(/\[\[\s+/, '[['), function (msg) {
        var parts = msg[0].content.split(/:/);
        ird = msg[0].inlinerolls[parts[1].match(/\d+/)];
        rdata = {
          order: parseInt(parts[0], 10),
          total:
            ird.results.total % 1 === 0
              ? ird.results.total
              : parseFloat(ird.results.total.toFixed(state[scriptName].config.maxDecimal)),
          rolls: _.reduce(
            ird.results.rolls,
            function (m, rs) {
              if ('R' === rs.type) {
                m.push({
                  sides: rs.sides,
                  rolls: _.pluck(rs.results, 'v'),
                });
              }
              return m;
            },
            []
          ),
        };

        rdata.bonus =
          ird.results.total -
          _.reduce(
            rdata.rolls,
            function (m, r) {
              m += _.reduce(
                r.rolls,
                function (s, dieroll) {
                  return s + dieroll;
                },
                0
              );
              return m;
            },
            0
          );

        rdata.bonus =
          rdata.bonus % 1 === 0 ? rdata.bonus : parseFloat(rdata.bonus.toFixed(state[scriptName].config.maxDecimal));

        turnEntries.push(rdata);

        finalize();
      });
    });
  };

  const handleInput = (msg_orig) => {
    var msg = _.clone(msg_orig),
      prev = Campaign().get('turnorder'),
      args,
      cmds,
      workgroup,
      workvar,
      error = false,
      cont = false,
      manualBonus = 0,
      manualBonusMin = 0,
      isReroll = false;
    const who = (getObj('player', msg.playerid) || { get: () => 'API' }).get('_displayname');

    let context = {
      who,
      playerid: msg.playerid,
    };

    let ids = [];

    if (msg.selected) {
      ids = [...ids, ...msg.selected.map((o) => o._id)];
    }

    if (msg.type !== 'api') {
      return;
    }

    if (_.has(msg, 'inlinerolls')) {
      msg.content = _.chain(msg.inlinerolls)
        .reduce(function (m, v, k) {
          m['$[[' + k + ']]'] = v.results.total || 0;
          return m;
        }, {})
        .reduce(function (m, v, k) {
          return m.replace(k, v);
        }, msg.content)
        .value();
    }

    args = msg.content.split(/\s+--/);
    switch (args.shift()) {
      case '!anima-init':
        if (args.length > 0) {
          cmds = args.shift().split(/\s+/);

          switch (cmds[0]) {
            case 'help':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              showHelp(msg.playerid);
              break;

            case 'ids':
              if (playerIsGM(msg.playerid) || msg.playerid === 'api') {
                ids = [...new Set([...ids, ...cmds.slice(1)])];
                cont = true;
              }
              break;

            case 'stack':
              {
                if (!playerIsGM(msg.playerid)) {
                  return;
                }
                cmds.shift();
                let operation = cmds.shift(),
                  showdate = function (ms) {
                    let ds = Math.round((_.now() - ms) / 1000),
                      str = [];

                    if (ds > 86400) {
                      str.push(`${Math.round(ds / 86400)}d`);
                      ds %= 86400;
                    }
                    if (ds > 3600) {
                      str.push(`${Math.round(ds / 3600)}h`);
                      ds %= 3600;
                    }

                    if (ds > 60) {
                      str.push(`${Math.round(ds / 60)}m`);
                      ds %= 60;
                    }
                    str.push(`${Math.round(ds)}s`);

                    return str.join(' ');
                  },
                  stackrecord = function (label) {
                    let toRaw = Campaign().get('turnorder'),
                      to = JSON.parse(toRaw) || [],
                      summary = _.chain(to)
                        .map((o) => {
                          return {
                            entry: o,
                            token: getObj('graphic', o.id),
                          };
                        })
                        .map((o) => {
                          return {
                            img: o.token ? o.token.get('imgsrc') : '',
                            name: o.token ? o.token.get('name') : o.entry.custom,
                            pr: o.entry.pr,
                          };
                        })
                        .value();

                    return {
                      label: label || (to.length ? `{${to.length} records}` : '{empty}'),
                      date: _.now(),
                      summary: summary,
                      turnorder: toRaw,
                    };
                  },
                  toMiniDisplay = function (summary) {
                    return (
                      '<div style="border: 1px solid #ccc;border-radius:.5em;padding:.5em;background-color:#eee;">' +
                      _.map(summary, (sume) => {
                        return `<div style="border-bottom: 1px solid #ccc;clear:both;"><div style="float:right;font-weight:bold;">${
                          sume.pr
                        }</div><img style="max-height:1.5em;float:left;" src="${sume.img}">${
                          sume.name || '&' + 'nbsp;'
                        }</div>`;
                      }).join('') +
                      '</div>'
                    );
                  },
                  stacklist = function () {
                    sendChat(
                      '',
                      `/w "${who}" ` +
                        '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;"><ol>' +
                        _.map(
                          state[scriptName].savedTurnOrders,
                          (o) => `<li>${o.label} [${showdate(o.date)}]${toMiniDisplay(o.summary)}</li>`
                        ).join('') +
                        '</ol></div>'
                    );
                  };
                switch (operation) {
                  case 'dup':
                  case 'copy':
                    // take current Turn Order and put it on top.
                    state[scriptName].savedTurnOrders.push(stackrecord(cmds.join(' ')));
                    stacklist();
                    break;
                  case 'push':
                    // take current Turn Order and put it on top.
                    state[scriptName].savedTurnOrders.push(stackrecord(cmds.join(' ')));
                    Campaign().set('turnorder', '[]');
                    notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                    stacklist();
                    break;
                  case 'pop':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders.pop();
                      Campaign().set('turnorder', sto.turnorder);
                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    } else {
                      sendChat(
                        '!anima-init --stack pop',
                        `/w "${who}" ` +
                          '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                          'No Saved Turn Orders to restore!' +
                          '</div>'
                      );
                    }
                    break;
                  case 'apply':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders[0];
                      Campaign().set('turnorder', sto.turnorder);
                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    } else {
                      sendChat(
                        '!anima-init --stack pop',
                        `/w "${who}" ` +
                          '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                          'No Saved Turn Orders to apply!' +
                          '</div>'
                      );
                    }
                    break;
                  case 'rot':
                  case 'rotate':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders.shift();
                      state[scriptName].savedTurnOrders.push(stackrecord(cmds.join(' ')));
                      Campaign().set('turnorder', sto.turnorder);
                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    }
                    break;
                  case 'rrot':
                  case 'reverse-rotate':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders.pop();
                      state[scriptName].savedTurnOrders.unshift(stackrecord(cmds.join(' ')));
                      Campaign().set('turnorder', sto.turnorder);
                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    }
                    break;
                  case 'swap':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders.shift();
                      state[scriptName].savedTurnOrders.unshift(stackrecord(cmds.join(' ')));
                      Campaign().set('turnorder', sto.turnorder);
                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    }
                    break;
                  case 'tswap':
                  case 'tail-swap':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders.pop();
                      state[scriptName].savedTurnOrders.push(stackrecord(cmds.join(' ')));
                      Campaign().set('turnorder', sto.turnorder);
                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    }
                    break;
                  case 'amerge':
                  case 'apply-merge':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders[0];

                      Campaign().set(
                        'turnorder',
                        JSON.stringify(
                          sorters[state[scriptName].config.sortOption].func(
                            _.union(JSON.parse(Campaign().get('turnorder')) || [], JSON.parse(sto.turnorder) || []),
                            state[scriptName].config.preserveFirst
                          )
                        )
                      );

                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    }
                    break;
                  case 'merge':
                    if (state[scriptName].savedTurnOrders.length) {
                      let sto = state[scriptName].savedTurnOrders.pop();

                      Campaign().set(
                        'turnorder',
                        JSON.stringify(
                          sorters[state[scriptName].config.sortOption].func(
                            _.union(JSON.parse(Campaign().get('turnorder')) || [], JSON.parse(sto.turnorder) || []),
                            state[scriptName].config.preserveFirst
                          )
                        )
                      );

                      notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
                      stacklist();
                    }
                    break;

                  case 'clear':
                    state[scriptName].savedTurnOrders = [];
                    break;

                  default:
                  case 'list':
                    stacklist();
                    break;
                }
              }
              break;

            case 'promote':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              cmds[1] = Math.max(parseInt(cmds[1], 10), 1);
              if (state[scriptName].bonusStatGroups.length >= cmds[1]) {
                if (1 !== cmds[1]) {
                  workvar = state[scriptName].bonusStatGroups[cmds[1] - 1];
                  state[scriptName].bonusStatGroups[cmds[1] - 1] = state[scriptName].bonusStatGroups[cmds[1] - 2];
                  state[scriptName].bonusStatGroups[cmds[1] - 2] = workvar;
                }

                sendChat(scriptName, `/w "${who}" ${helpParts.showBonusStatGroupsConfig(context)}`);
              } else {
                sendChat(
                  '!anima-init --promote',
                  `/w "${who}" ` +
                    '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                    'Please specify one of the following by number:' +
                    helpParts.showBonusStatGroupsConfig(context) +
                    '</div>'
                );
              }
              break;

            case 'del-group':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              cmds[1] = Math.max(parseInt(cmds[1], 10), 1);
              if (state[scriptName].bonusStatGroups.length >= cmds[1]) {
                state[scriptName].bonusStatGroups = _.filter(state[scriptName].bonusStatGroups, function (v, k) {
                  return k !== cmds[1] - 1;
                });

                sendChat(scriptName, `/w "${who}" ${helpParts.showBonusStatGroupsConfig(context)}`);
              } else {
                sendChat(
                  '!anima-init --del-group',
                  `/w "${who}" ` +
                    '<div style="padding:1px 3px;bhttps://raytheon.benefitcenter.com/v3/client_docs/en_us/rth/HealthAdvocate_Top_Ten_Reasons.pdforder: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                    'Please specify one of the following by number:' +
                    helpParts.showBonusStatGroupsConfig(context) +
                    '</div>'
                );
              }
              break;

            case 'toggle-turnorder':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              if (false !== Campaign().get('initiativepage')) {
                Campaign().set({
                  initiativepage: false,
                });
              } else {
                let player = getObj('player', msg.playerid) || { get: () => true };
                let pid = player.get('_lastpage');
                if (!pid) {
                  pid = Campaign().get('playerpageid');
                }
                Campaign().set({
                  initiativepage: pid,
                });
              }
              break;

            case 'reroll':
              isReroll = true;
              if (cmds[1] && cmds[1].match(/^[-+]?\d+(\.\d+)?$/)) {
                manualBonus = parseFloat(cmds[1]) || 0;
              }

              ids = JSON.parse(Campaign().get('turnorder') || '[]')
                .filter((e) => '-1' !== e.id)
                .map((e) => e.id);

              cont = true;
              break;

            case 'sort':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              Campaign().set(
                'turnorder',
                JSON.stringify(
                  sorters[state[scriptName].config.sortOption].func(
                    JSON.parse(Campaign().get('turnorder')) || [],
                    false
                  )
                )
              );
              notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);

              break;

            case 'adjust':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              if (cmds[1] && cmds[1].match(/^[-+]?\d+(\.\d+)?$/)) {
                manualBonus = parseFloat(cmds[1]);
                manualBonusMin = parseFloat(cmds[2]);
                manualBonusMin = _.isNaN(manualBonusMin) ? -10000 : manualBonusMin;

                Campaign().set({
                  turnorder: JSON.stringify(
                    _.map(JSON.parse(Campaign().get('turnorder')) || [], function (e) {
                      if ('-1' !== e.id) {
                        e.pr = Math.max(
                          (_.isNaN(parseFloat(e.pr)) ? 0 : parseFloat(e.pr)) + manualBonus,
                          manualBonusMin
                        ).toFixed(state[scriptName].config.maxDecimal);
                      }
                      return e;
                    })
                  ),
                });
                notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
              } else {
                sendChat(
                  scriptName,
                  `/w "${who}" ` +
                    '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                    'Not a valid adjustment: <b>' +
                    cmds[1] +
                    '</b>' +
                    '</div>'
                );
              }
              break;

            case 'adjust-current':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              if (cmds[1] && cmds[1].match(/^[-+]?\d+(\.\d+)?$/)) {
                manualBonus = parseFloat(cmds[1]);
                manualBonusMin = parseFloat(cmds[2]);
                manualBonusMin = _.isNaN(manualBonusMin) ? -10000 : manualBonusMin;

                Campaign().set({
                  turnorder: JSON.stringify(
                    _.map(JSON.parse(Campaign().get('turnorder')) || [], function (e, idx) {
                      if (0 === idx && '-1' !== e.id) {
                        e.pr = Math.max(
                          (_.isNaN(parseFloat(e.pr)) ? 0 : parseFloat(e.pr)) + manualBonus,
                          manualBonusMin
                        ).toFixed(state[scriptName].config.maxDecimal);
                      }
                      return e;
                    })
                  ),
                });
                notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
              } else {
                sendChat(
                  scriptName,
                  `/w "${who}" ` +
                    '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                    'Not a valid adjustment: <b>' +
                    cmds[1] +
                    '</b>' +
                    '</div>'
                );
              }
              break;

            case 'clear':
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              Campaign().set({
                turnorder: '[]',
                initiativepage: state[scriptName].config.autoOpenInit ? false : Campaign().get('initiativepage'),
              });
              notifyObservers('turnOrderChange', Campaign().get('turnorder'), prev);
              break;

            case 'bonus':
              if (cmds[1] && cmds[1].match(/^[-+]?\d+(\.\d+)?$/)) {
                manualBonus = parseFloat(cmds[1]);
                cont = true;
              } else {
                sendChat(
                  scriptName,
                  `/w "${who}" ` +
                    '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                    'Not a valid bonus: <b>' +
                    cmds[1] +
                    '</b>' +
                    '</div>'
                );
              }
              break;

            default:
              if (!playerIsGM(msg.playerid)) {
                return;
              }
              sendChat(
                scriptName,
                `/w "${who}" ` +
                  '<div style="padding:1px 3px;border: 1px solid #8B4513;background: #eeffee; color: #8B4513; font-size: 80%;">' +
                  'Not a valid command: <b>' +
                  cmds[0] +
                  '</b>' +
                  '</div>'
              );
              break;
          }
        } else {
          cont = true;
        }

        if (cont) {
          if (ids.length) {
            makeRollsForIDs(ids, { isReroll, manualBonus, prev });
          } else {
            showHelp(msg.playerid);
          }
        }
        break;
      case '!anima-init-config':
        if (!playerIsGM(msg.playerid)) {
          return;
        }
        if (_.contains(args, '--help')) {
          showHelp(msg.playerid);
          return;
        }
        if (!args.length) {
          sendChat('', `/w "${who}" ${helpParts.helpConfig(context)}`);
          return;
        }
        _.each(args, function (a) {
          var opt = a.split(/\|/),
            omsg = '';

          switch (opt.shift()) {
            case 'sort-option':
              if (sorters[opt[0]]) {
                state[scriptName].config.sortOption = opt[0];
              } else {
                omsg = '<div><b>Error:</b> Not a valid sort method: ' + opt[0] + '</div>';
              }
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  omsg +
                  helpParts.sortOptionsConfig(context) +
                  '</div>'
              );
              break;

            case 'set-die-size':
              if (opt[0].match(/^\d+$/)) {
                state[scriptName].config.dieSize = parseInt(opt[0], 10);
              } else {
                omsg = '<div><b>Error:</b> Not a die size: ' + opt[0] + '</div>';
              }
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  omsg +
                  helpParts.dieSizeConfig(context) +
                  '</div>'
              );
              break;

            case 'set-max-decimal':
              if (opt[0].match(/^\d+$/)) {
                state[scriptName].config.maxDecimal = parseInt(opt[0], 10);
              } else {
                omsg = '<div><b>Error:</b> Not a valid decimal count: ' + opt[0] + '</div>';
              }
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  omsg +
                  helpParts.maxDecimalConfig(context) +
                  '</div>'
              );
              break;

            case 'toggle-auto-open-init':
              state[scriptName].config.autoOpenInit = !state[scriptName].config.autoOpenInit;
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  helpParts.autoOpenInitConfig(context) +
                  '</div>'
              );
              break;

            case 'toggle-replace-roll':
              state[scriptName].config.replaceRoll = !state[scriptName].config.replaceRoll;
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  helpParts.replaceRollConfig(context) +
                  '</div>'
              );
              break;

            case 'toggle-preserve-first':
              state[scriptName].config.preserveFirst = !state[scriptName].config.preserveFirst;
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  helpParts.preserveFirstConfig(context) +
                  '</div>'
              );
              break;

            case 'set-announcer':
              if (announcers[opt[0]]) {
                state[scriptName].config.announcer = opt[0];
              } else {
                omsg = '<div><b>Error:</b> Not a valid announcer: ' + opt[0] + '</div>';
              }
              sendChat(
                '',
                `/w "${who}" ` +
                  '<div style="border: 1px solid black; background-color: white; padding: 3px 3px;">' +
                  omsg +
                  helpParts.announcerConfig(context) +
                  '</div>'
              );
              break;

            default:
              sendChat('', `/w "${who}" ` + '<div><b>Unsupported Option:</div> ' + a + '</div>');
          }
        });

        break;
    }
  };

  const registerEventHandlers = function () {
    on('chat:message', handleInput);
  };

  on('ready', () => {
    initScript();
    registerEventHandlers();
  });

  return {
    ObserveTurnOrderChange: observeTurnOrderChange,
    RollForTokenIDs: rollForTokenIDsExternal,
  };
})();
