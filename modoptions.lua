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
    name   = 'Minimum acceleration',
    desc   = "Land, sea and hover units accelerate at least this fast (TA's are 0.003 to 0.2; 1 reaches top speed in a few frames). 0 keeps TA's.\nkey: moveaccel",
    type   = 'number',
    section= 'movement',
    def    = 0,
    min    = 0,
    max    = 1,
    step   = 0.05,
  },

  {
    key    = 'movebrake',
    name   = 'Minimum braking',
    desc   = "Land, sea and hover units brake at least this fast (TA's are 0.002 to 1, most under 0.1). Quick stops are what make dodging work. 0 keeps TA's.\nkey: movebrake",
    type   = 'number',
    section= 'movement',
    def    = 0,
    min    = 0,
    max    = 1,
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
    desc   = "Projectiles at or under the cutoff below (torpedoes, light and medium cannons, E.M.G.s, flamethrower, D-Gun...) fly this many times TA's speed, so faster units cannot simply outrun them. Damage and range are unchanged; cannon arcs get flatter. 1 keeps TA's.\nkey: shotspeed",
    type   = 'number',
    section= 'movement',
    def    = 1.25,
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
