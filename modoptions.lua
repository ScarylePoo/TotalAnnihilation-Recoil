--  Custom Options Definition Table format

--  NOTES:
--  - using an enumerated table lets you specify the options order

--
--  These keywords must be lowercase for LuaParser to read them.
--
--  key:      the string used in the script.txt
--  name:     the displayed name
--  desc:     the description (could be used as a tooltip)
--  type:     the option type
--  def:      the default value
--  min:      minimum value for number options
--  max:      maximum value for number options
--  step:     quantization step, aligned to the def value
--  maxlen:   the maximum string length for string options
--  items:    array of item strings for list options
--  scope:    'global', 'player', 'team', 'allyteam'
--

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------


local options =
{
	{
    key    = 'botagame',
    name   = 'Main options',
    desc   = 'Main game options',
    type   = 'section',
	},

	{
		key="mode", -- read by game_end.lua and game_com_ends.lua
		name="Game End Mode",
		desc="What it takes to eliminate a player or team\nkey: mode",
		type="list",
		section= 'botagame',
		def="comends",
		items={
			{key="commander", name="Commander Ends", desc="Player will die if commander is killed"},
			{key="comends", name="Team Commander Ends", desc="Team will die if commanders of all players are killed."},
			{key="killall", name="Kill all enemy players", desc="Kill all enemies. Player will die if they have no units left."},
			{key="team", name="Kill all enemy units", desc="Kill all enemies. Dead players are retained until whole team dies"},
		},
	},

  {
    key    = 'StartingResources',
    name   = 'Starting Resources',
    desc   = 'Sets storage and amount of resources that players will start with',
    type   = 'section',
  },

  {
		key		= "debugmode",
		name	= "Debug Mode",
		desc	= "Enable debugging mode. Will allow /cheat by default, and load gadget profiler.\nkey: debugmode",
		type	= "bool",
		section	= 'botagame',
		def		= false,
	},

	{
		key		= "factionchoice", -- read by luarules/gadgets/game_spawn.lua
		name	= "Faction Choice",
		desc	= "Players pick Arm or Core at the start of the game. Off: each player gets the side set in the lobby (random when none).\nkey: factionchoice",
		type	= "bool",
		section	= 'botagame',
		def		= true,
	},

	{
		key		= "startplacement", -- read by luarules/gadgets/game_spawn.lua
		name	= "Start Placement",
		desc	= "Players pick a start spot on the map at the start of the game. Off: commanders appear at the lobby or start box positions.\nkey: startplacement",
		type	= "bool",
		section	= 'botagame',
		def		= true,
	},
  
  {
    key    = 'StartMetal',
    name   = 'Starting metal',
    desc   = 'Determines amount of metal and metal storage that each player will start with',
    type   = 'number',
    section= 'StartingResources',
    def    = 1000,
    min    = 0,
    max    = 10000,
    step   = 1,  -- quantization is aligned to the def value
                    -- (step <= 0) means that there is no quantization
  },
  {
   key    = 'StartMetal',
   scope  = 'team',
   name   = 'Team Starting metal',
   desc   = 'Determines amount of metal and metal storage this team will start with',
   type   = 'number',
   section= 'StartingResources',
   def    = 1000,
   min    = 0,
   max    = 10000,
   step   = 1,  -- quantization is aligned to the def value
   -- (step <= 0) means that there is no quantization
  },
  {
    key    = 'StartEnergy',
    name   = 'Starting energy',
    desc   = 'Determines amount of energy and energy storage that each player will start with',
    type   = 'number',
    section= 'StartingResources',
    def    = 1000,
    min    = 0,
    max    = 10000,
    step   = 1,  -- quantization is aligned to the def value
                    -- (step <= 0) means that there is no quantization
  },
  {
   key    = 'StartEnergy',
   scope  = 'team',
   name   = 'Team Starting energy',
   desc   = 'Determines amount of energy and energy storage that this team will start with',
   type   = 'number',
   section= 'StartingResources',
   def    = 1000,
   min    = 0,
   max    = 10000,
   step   = 1,  -- quantization is aligned to the def value
   -- (step <= 0) means that there is no quantization
  },

  {
    key    = 'MaxUnits',
    name   = 'Max units',
    desc   = 'Maximum number of units (including buildings) for each team allowed at the same time',
    type   = 'number',
    def    = 1000,
    min    = 1,
    max    = 10000, --- engine caps at lower limit if more than 3 team are ingame
    step   = 1,  -- quantization is aligned to the def value
                    -- (step <= 0) means that there is no quantization
  },

  {
    key    = 'LimitDgun',
    name   = 'Limit D-Gun range',
    desc   = "The commander's D-Gun weapon will be usable only close to the player's starting location",
    type   = 'bool',
    def    = false,
  },

  {
    key    = 'GhostedBuildings',
    name   = 'Ghosted buildings',
    desc   = "Once an enemy building will be spotted\na ghost trail will be placed to memorize location even after the loss of the line of sight",
    type   = 'bool',
    def    = true,
  },
  {
    key    = 'DiminishingMMs',
    name   = 'Diminishing metal makers efficiency',
    desc   = "Everytime a new metal maker will be built, the energy/metal efficiency ratio will decrease",
    type   = 'bool',
    def    = false,
  },

  {
    key    = 'FixedAllies',
    name   = 'Fixed ingame alliances',
    desc   = 'Disables the possibility of players to dynamically change alliances ingame',
    type   = 'bool',
    def    = false,
  },

  {
    key    = 'LimitSpeed',
    name   = 'Speed Restriction',
    desc   = 'Limits maximum and minimum speed that the players will be allowed to change to',
    type   = 'section',
  },

  {
    key    = 'MaxSpeed',
    name   = 'Maximum game speed',
    desc   = 'Sets the maximum speed that the players will be allowed to change to',
    type   = 'number',
    section= 'LimitSpeed',
    def    = 3,
    min    = 0.1,
    max    = 100,
    step   = 0.1,  -- quantization is aligned to the def value
                    -- (step <= 0) means that there is no quantization
  },

  {
    key    = 'MinSpeed',
    name   = 'Minimum game speed',
    desc   = 'Sets the minimum speed that the players will be allowed to change to',
    type   = 'number',
    section= 'LimitSpeed',
    def    = 0.3,
    min    = 0.1,
    max    = 100,
    step   = 0.1,  -- quantization is aligned to the def value
                    -- (step <= 0) means that there is no quantization
  },

  {
    key    = 'movement',
    name   = 'Movement',
    desc   = 'How fast and how nimbly units move',
    type   = 'section',
  },

  {
    key    = 'movespeed', -- read by gamedata/alldefs_post.lua (land, sea and hover units; aircraft unchanged)
    name   = 'Ground unit speed',
    desc   = "Top speed of land, sea and hover units, as a multiple of TA's. Aircraft are unchanged. Walk animations keep pace.\nkey: movespeed",
    type   = 'number',
    section= 'movement',
    def    = 1.25,
    min    = 1,
    max    = 2,
    step   = 0.05,
  },

  {
    key    = 'moveturn',
    name   = 'Ground unit turn rate',
    desc   = "Turn rate of land, sea and hover units, as a multiple of TA's. Keep it level with the speed so turning circles stay TA's size.\nkey: moveturn",
    type   = 'number',
    section= 'movement',
    def    = 1.25,
    min    = 1,
    max    = 2,
    step   = 0.05,
  },

  {
    key    = 'moveaccel',
    name   = 'Ground unit acceleration',
    desc   = "Land, sea and hover units' acceleration x this (TA's values are 0.003 to 0.2 elmos/frame^2; the engine floors them at 0.01). 1 keeps TA's (1.5 play-tested).\nkey: moveaccel",
    type   = 'number',
    section= 'movement',
    def    = 1.5,
    min    = 0.25,
    max    = 4,
    step   = 0.05,
  },

  {
    key    = 'movebrake',
    name   = 'Ground unit braking',
    desc   = "Land, sea and hover units' brake rate x this (TA's values are 0.002 to 1, most under 0.1; the engine floors them at 0.01). Quick stops are what make dodging work. 1 keeps TA's (1.5 play-tested).\nkey: movebrake",
    type   = 'number',
    section= 'movement',
    def    = 1.5,
    min    = 0.25,
    max    = 4,
    step   = 0.05,
  },

  {
    key    = 'moveturninplace',
    name   = 'Turn in place above',
    desc   = "Degrees: a land, sea or hover unit turning by more than this slows down to pivot; a smaller turn is taken at speed, in a curve. 0 is the engine's default (every turn slows the unit; with quick braking it stops dead).\nkey: moveturninplace",
    type   = 'number',
    section= 'movement',
    def    = 90,
    min    = 0,
    max    = 180,
    step   = 5,
  },

  {
    key    = 'shotspeed', -- read by gamedata/alldefs_post.lua (WeaponDef_Post)
    name   = 'Slow projectile speed',
    desc   = "Projectiles at or under the cutoff below (torpedoes, light and medium cannons, E.M.G.s, flamethrower, D-Gun...) fly this many times TA's speed, so faster units cannot simply outrun them. Damage and range are unchanged; cannon arcs get flatter. 1 keeps TA's (1.5 play-tested).\nkey: shotspeed",
    type   = 'number',
    section= 'movement',
    def    = 1.5,
    min    = 1,
    max    = 2,
    step   = 0.05,
  },

  {
    key    = 'shotspeedcutoff',
    name   = 'Slow projectile cutoff',
    desc   = "Elmos per second: weapons whose TA projectile speed is this or less get the speed multiplier above (300 takes in everything up to the E.M.G.; the next fastest are the Luger, Pillager and Immolator at 310).\nkey: shotspeedcutoff",
    type   = 'number',
    section= 'movement',
    def    = 300,
    min    = 0,
    max    = 1000,
    step   = 10,
  },

  {
    key    = 'ranges',
    name   = 'Ranges',
    desc   = 'Weapon and sight ranges',
    type   = 'section',
  },

  {
    key    = 'weaponrange', -- read by gamedata/alldefs_post.lua (WeaponDef_Post)
    name   = 'Weapon range',
    desc   = "Every weapon's range, as a multiple of TA's. Longer ranges let more of a group fire without crowding forward. Missile flight times and cannon speeds scale so they still reach. Raise sight with it, or units outrange what they can see.\nkey: weaponrange",
    type   = 'number',
    section= 'ranges',
    def    = 1.25,
    min    = 1,
    max    = 2,
    step   = 0.05,
  },

  {
    key    = 'sightrange', -- read by gamedata/alldefs_post.lua (UnitDef_Post)
    name   = 'Sight range',
    desc   = "Every unit's sight radius, as a multiple of TA's (air sight follows). Radar and sonar are unchanged.\nkey: sightrange",
    type   = 'number',
    section= 'ranges',
    def    = 1.25,
    min    = 1,
    max    = 2,
    step   = 0.05,
  },

  {
    key    = 'buildrange', -- read by gamedata/alldefs_post.lua (UnitDef_Post)
    name   = 'Build range',
    desc   = "How far builders reach when building, repairing and reclaiming, as a multiple of TA's (TA 3.1c: 40 to 100 elmos). The bigger footprints need more than TA's reach to start a building.\nkey: buildrange",
    type   = 'number',
    section= 'ranges',
    def    = 1.5,
    min    = 1,
    max    = 3,
    step   = 0.05,
  },

  {
    key    = 'ai',
    name   = 'AI',
    desc   = 'The built-in Lua AIs (AdaptiveAI, SimpleAI)',
    type   = 'section',
  },

  {
    key    = 'adaptiveai_start', -- read by luarules/configs/simpleai/behaviors/b_adaptive.lua
    name   = 'AdaptiveAI starting difficulty',
    desc   = "Where the AdaptiveAI starts before it has read the game: 0 easiest, 0.5 plain SimpleAI, 1 hardest. From 3 minutes in it reads the game every 30 seconds and hardens quickly (eases slowly) to keep the edge set below.\nkey: adaptiveai_start",
    type   = 'number',
    section= 'ai',
    def    = 0.6,
    min    = 0,
    max    = 1,
    step   = 0.05,
  },

  {
    key    = 'adaptiveai_edge', -- read by luarules/configs/simpleai/behaviors/b_adaptive.lua
    name   = 'AdaptiveAI edge',
    desc   = "How far ahead of you the AdaptiveAI tries to stay (army value, kills, income, pressure, as a share of the total: 0.15 is about 57/43 in its favour). 0 steers for an even game.\nkey: adaptiveai_edge",
    type   = 'number',
    section= 'ai',
    def    = 0.15,
    min    = 0,
    max    = 0.5,
    step   = 0.05,
  },

  {
    key    = 'adaptiveai_aggression', -- read by luarules/configs/simpleai/behaviors/b_adaptive.lua
    name   = 'AdaptiveAI aggression',
    desc   = "How willing the AdaptiveAI is to attack and to see an attack through, whatever it costs. 0 is cautious: it waits for a big advantage and pulls back early. 0.5 is the old behaviour. 1 is reckless: it attacks on less than your army, fights on while outnumbered and hurt, and only turns back when it is losing more than you are. Separate from difficulty, and it does not change during the game.\nkey: adaptiveai_aggression",
    type   = 'number',
    section= 'ai',
    def    = 0.7,
    min    = 0,
    max    = 1,
    step   = 0.05,
  },

  {
    key    = 'ai_neverstall',
    name   = 'AI never stalls',
    desc   = "Keeps SimpleAI teams' metal and energy from running dry (a small floor, 150 of each). AdaptiveAI always has it.\nkey: ai_neverstall",
    type   = 'list',
    section= 'ai',
    def    = 'enabled',
    items  = {
      { key = 'disabled', name = 'Disabled', desc = 'A clean, non-cheating AI' },
      { key = 'enabled',  name = 'Enabled',  desc = 'The AI is topped up to 150 metal and energy whenever it drops below' },
    },
  },

  {
    key    = 'aitrace',
    name   = 'AI decision trace in the log',
    desc   = "Writes each AI team's decision trace to the infolog every 10 seconds (what it built and why). For debugging.\nkey: aitrace",
    type   = 'bool',
    section= 'ai',
    def    = false,
  },

  --------------------------------------------------------------------------------
  -- Survival AI (luarules/gadgets/ai_survival.lua; ported from Splinter Faction)
  --------------------------------------------------------------------------------

	{
		key    = 'survivalaioptions',
		name   = 'Survival AI Options',
		desc   = 'Allows you to control at a granular level the individual options for the Survival AI',
		type   = 'section',
	},
	{
		key="survivalaidifficulty",
		name="Survival AI Difficulty",
		desc="How hard should the Survival AI be?",
		type="list",
		def="normal",
		section="survivalaioptions",
		items={
			{key="easy", name="Easy", desc="Lower plateau, a later ramp, no late creep, and waves arrive 25% slower."},
			{key="normal", name="Normal", desc="Baseline curve and cadence. A good player out-produces the plateau and clears the network."},
			{key="hard", name="Hard", desc="Higher plateau, an earlier ramp, a real late creep, and waves arrive 10% faster."},
			{key="impossibru", name="Impossibru", desc="Far higher plateau, a much earlier ramp, a relentless late creep, waves 25% faster. I'm sure someone out there can beat it, but that person isn't you."},
		}
	},
	{
		key     = "survivalai_graceperiod",
		name    = "Grace Period (seconds)",
		desc    = "Calm before the first wave arrives, counted from the end of placement.",
		type    = "number",
		def     = 180,
		min     = 0,
		max     = 900,
		step    = 30,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_waveinterval",
		name    = "Wave Interval (seconds)",
		desc    = "Seconds between waves. Lower = relentless pressure.",
		type    = "number",
		def     = 60,
		min     = 15,
		max     = 300,
		step    = 5,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_t2minutes",
		name    = "Tech 2 Unlock (minutes)",
		desc    = "Minutes on the wave clock before Tech 2 units join the waves.",
		type    = "number",
		def     = 10,
		min     = 0,
		max     = 60,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_t3minutes",
		name    = "Tech 3 Unlock (minutes)",
		desc    = "Minutes on the wave clock before Tech 3 units join the waves.",
		type    = "number",
		def     = 25,
		min     = 0,
		max     = 90,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_basebudget",
		name    = "Base Wave Budget (metal)",
		desc    = "Metal value of the first wave with the full beacon network standing, before the difficulty multiplier.",
		type    = "number",
		def     = 300,
		min     = 100,
		max     = 10000,
		step    = 50,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_peakbudget",
		name    = "Peak Wave Budget (metal)",
		desc    = "The plateau the wave budget levels off at, before the difficulty multiplier. This is the main difficulty dial for the mid and late game.",
		type    = "number",
		def     = 5000,
		min     = 1000,
		max     = 100000,
		step    = 500,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_rampminutes",
		name    = "Budget Ramp Midpoint (minutes)",
		desc    = "Minute on the wave clock at which the budget is halfway from base to peak. Lower = the pressure arrives sooner.",
		type    = "number",
		def     = 14,
		min     = 3,
		max     = 60,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_latecreep",
		name    = "Late Budget Creep (metal per minute)",
		desc    = "Metal added to the budget every minute once the plateau is reached, before the difficulty multiplier. 0 = a true plateau.",
		type    = "number",
		def     = 60,
		min     = 0,
		max     = 5000,
		step    = 25,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_fieldcap",
		name    = "Field Cap (wave budgets)",
		desc    = "How many wave budgets' worth of metal the Survival AI may have alive at once. Each wave only tops the field up to this cap, so uncleared units make the next wave smaller.",
		type    = "number",
		def     = 2.0,
		min     = 1,
		max     = 6,
		step    = 0.25,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_maxwaveunits",
		name    = "Max Units Per Wave",
		desc    = "Hard cap on units in a single wave per survival team. Raise for late-game spectacle, lower for performance.",
		type    = "number",
		def     = 40,
		min     = 10,
		max     = 200,
		step    = 5,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_networksize",
		name    = "Beacon Network Size",
		desc    = "Beacons the Survival AI starts with (fewer if the map is too tight). The network never grows past this.",
		type    = "number",
		def     = 8,
		min     = 1,
		max     = 16,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_respawnminutes",
		name    = "Beacon Regrowth Timer (minutes)",
		desc    = "When the network is below full strength, a new beacon appears this long after the countdown starts. The countdown restarts after each new beacon. 0 disables regrowth.",
		type    = "number",
		def     = 10,
		min     = 0,
		max     = 60,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_beaconbounty",
		name    = "Beacon Bounty (metal)",
		desc    = "Metal paid to the team that destroys a beacon, with four times as much energy. The full amount from minute 15; 40% of it at the start. 0 = no bounty.",
		type    = "number",
		def     = 1500,
		min     = 0,
		max     = 2000,
		step    = 50,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_retaliationdelay",
		name    = "Retaliation Delay (seconds)",
		desc    = "Seconds after a beacon dies before its nearest neighbors launch a half-strength counterattack at the killer.",
		type    = "number",
		def     = 5,
		min     = 0,
		max     = 300,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_creepmin",
		name    = "Beacon Regrowth Min Distance",
		desc    = "Minimum distance (elmos) a regrown beacon spawns from its source beacon.",
		type    = "number",
		def     = 900,
		min     = 200,
		max     = 4000,
		step    = 100,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_creepmax",
		name    = "Beacon Regrowth Max Distance",
		desc    = "Maximum distance (elmos) a regrown beacon spawns from its source beacon -- the leash.",
		type    = "number",
		def     = 3000,
		min     = 400,
		max     = 8000,
		step    = 100,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_factionpure",
		name    = "Faction-Pure Wave Chance",
		desc    = "Chance a wave draws from a single side only (all Arm or all Core) (0 = always mixed, 1 = always pure).",
		type    = "number",
		def     = 0.25,
		min     = 0,
		max     = 1,
		step    = 0.05,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_specialchance",
		name    = "Special Beacon Chance",
		desc    = "Share of beacons (other than the master) that are specialized (jammer / accelerator / forge) instead of standard.",
		type    = "number",
		def     = 0.6,
		min     = 0,
		max     = 1,
		step    = 0.05,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_garrison",
		name    = "Garrison Turrets Per Beacon",
		desc    = "Defense turrets around every beacon. Tech 1 turrets from the start, replaced by Tech 2 turrets when Tech 2 unlocks. 0 disables garrisons.",
		type    = "number",
		def     = 3,
		min     = 0,
		max     = 8,
		step    = 1,
		section = "survivalaioptions",
	},
	{
		key     = "survivalai_surgewaves",
		name    = "Surge Wave Interval",
		desc    = "Every Nth wave is a surge: double budget, a dramatic archetype, launched from every beacon at once, announced one wave in advance. 0 disables surges.",
		type    = "number",
		def     = 10,
		min     = 0,
		max     = 50,
		step    = 1,
		section = "survivalaioptions",
	},
  {
    key    = 'DisableMapDamage',
    name   = 'Undeformable map',
    desc   = 'Prevents the map shape from being changed by weapons',
    type   = 'bool',
    def    = false,
  },
  {
    key    = 'allowuserwidgets',
    name   = 'Allow User Widgets',
    desc   = "Load loose widgets from LuaUI/Widgets in each player's data directory (the widget handler, from Splinter Faction, ignores them otherwise: in an install shared with other games their widgets would load into TA:Recoil and break its interface).",
    type   = 'bool',
    def    = false,
  },

}

return options
