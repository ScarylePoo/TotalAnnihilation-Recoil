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
