--------------------------------------------------------------------------------
-- alldefs_post.lua: ALL unit and weapon def post-processing of the game lives here
--------------------------------------------------------------------------------
-- Same layout as Splinter Faction:
--   gamedata/unitdefs_post.lua   runs the engine's own unit post-processing, then calls UnitDef_Post for every unit
--   gamedata/weapondefs_post.lua runs the engine's own weapon post-processing (it turns TA tags such as lineofsight,
--                                ballistic, rendertype into weapontype etc.), then calls WeaponDef_Post for every weapon
-- Both include this file, so put any def tweak in UnitDef_Post / WeaponDef_Post below, not in those two files.
-- Unlike SF, TA:Recoil keeps its weapons in standalone files (Weapons/*.lua), so there are no weapondefs inside unit
-- defs to extract. Armor classes: gamedata/ArmorDefs.lua; movement classes: gamedata/movedefs.lua.
--------------------------------------------------------------------------------

function tobool(val)
	local t = type(val)
	if (t == 'nil') then
		return false
	elseif (t == 'boolean') then
		return val
	elseif (t == 'number') then
		return (val ~= 0)
	elseif (t == 'string') then
		return ((val ~= '0') and (val ~= 'false'))
	end
	return false
end

--------------------------------------------------------------------------------
-- UNITS
--------------------------------------------------------------------------------

-- Commanders: read by luarules/gadgets/game_com_ends.lua (game end modes
-- "commander" and "comends"). Decoy commanders are deliberately not listed.
local COMMANDERS = {
	arm_commander  = true,
	core_commander = true,
}

function UnitDef_Post(name, ud)
	-- TA units did not regenerate; the engine's default is 10 HP/s after idleTime. Units without the tag get none.
	if ud.idleautoheal == nil then
		ud.idleautoheal = 0
	end
	if COMMANDERS[name] then
		ud.customparams = ud.customparams or {}
		ud.customparams.iscommander = 1
	end
	-- Air repair pads: the engine ignores isairbase, luarules/gadgets/unit_air_pads.lua reads this.
	if ud.isairbase then
		ud.customparams = ud.customparams or {}
		ud.customparams.isairbase = 1
	end
end

--------------------------------------------------------------------------------
-- WEAPONS
--------------------------------------------------------------------------------

-- TA tags the engine has no use for (TA's own effects, ids, smoke and screen
-- shake, guidance flags). Stripped so the log only shows real problems.
local TA_ONLY_TAGS = {
  'id', 'explosionart', 'explosiongaf', 'waterexplosionart', 'waterexplosiongaf',
  'lavaexplosionart', 'lavaexplosiongaf', 'startsmoke', 'endsmoke', 'smokedelay',
  'shakemagnitude', 'shakeduration', 'minbarrelangle', 'selfprop', 'guidance',
  'bursttime', 'toairweapon', 'randomdecay', 'pitchtolerance',
}

local explosiveWeapons = {
	MissileLauncher = true,
	StarburstLauncher = true,
	TorpedoLauncher = true,
	Cannon = true,
	AircraftBomb = true,
}
local inertialessWeapons = {
	LaserCannon = true,
	BeamLaser = true,
	EmgCannon = true,
	Flame = true,
	LightningCannon = true,
	DGun = true,
}

local modOptions = Spring.GetModOptions and Spring.GetModOptions() or {}

-- Cannon ballistics as in TA 3.1c: the weapon's own weaponvelocity under TA's standard gravity. 85 of the 95 TA maps
-- set gravity=112 in their .ota (elmos/s^2, i.e. 112/900 per frame^2), and TA's cannons were designed for it: their
-- v^2/g is ~1.16x their range (median), so they reach it on a ~30-45 degree arc. Fixed per weapon (mygravity) so arcs
-- do not change with the map. (BOTA instead used gravity 0.25 and recomputed every velocity from the range.)
local TA_GRAVITY = 112 / 900

-- Plasma ball size by damage per shot (largest of default/planes): ~2.5 for the 8-damage EMG, 16 for the
-- 2400-damage Intimidator, square-root curve so the mid-weight tank guns stay modest (130 damage -> ~5.5).
local SIZE_MIN, SIZE_MAX, DMG_MIN, DMG_MAX = 2.5, 16, 8, 2400
-- Laser bolts (every laser is a LaserCannon: TA had no continuous beams). One look for all of them, scaled by damage:
-- thin bright bolts for light lasers, heavier ones up to the Annihilator; a white-hot core in a tint of the laser's
-- colour; colours clamped to 0..1 (BOTA had components of 4).
local function Clamp01(x) return math.min(math.max(x, 0), 1) end
local function ParseColor(c)
	if type(c) == "table" then return { tonumber(c[1]) or 1, tonumber(c[2]) or 1, tonumber(c[3]) or 1 } end
	local r, g, b = tostring(c or ""):match("([%d%.]+)%s+([%d%.]+)%s+([%d%.]+)")
	if not r then return nil end
	return { tonumber(r), tonumber(g), tonumber(b) }
end
local function LaserLook(wd)
	local d = 0
	for _, v in pairs(wd.damage or {}) do d = math.max(d, tonumber(v) or 0) end
	local f = math.sqrt(math.min(math.max((d - 8) / (2500 - 8), 0), 1))
	wd.thickness = 1.5 + 2.5 * f
	wd.corethickness = 0.4
	wd.laserflaresize = 5 + 5 * f
	local c1 = ParseColor(wd.rgbcolor) or { 1, 0, 0 }
	for i = 1, 3 do c1[i] = Clamp01(c1[i]) end
	-- the core: the outer colour pushed most of the way to white, so a red laser has a pink-white core
	local c2 = {}
	for i = 1, 3 do c2[i] = Clamp01(c1[i] + (1 - c1[i]) * 0.7) end
	wd.rgbcolor = ("%.3f %.3f %.3f"):format(c1[1], c1[2], c1[3])
	wd.rgbcolor2 = ("%.3f %.3f %.3f"):format(c2[1], c2[2], c2[3])
	wd.hardstop = true
end

local function CannonSize(wd)
	local d = 0
	for _, v in pairs(wd.damage or {}) do d = math.max(d, tonumber(v) or 0) end
	local f = math.min(math.max((d - DMG_MIN) / (DMG_MAX - DMG_MIN), 0), 1)
	return SIZE_MIN + (SIZE_MAX - SIZE_MIN) * math.sqrt(f)
end
local interceptorStyle = 2
if modOptions and modOptions.nuke and not tobool(modOptions.nuke) then interceptorStyle = 1 end


-- Cannon trail (from Splinter Faction's alldefs_post): a short flame CEG behind every cannon shell
-- (gamedata/explosions/plasmacannontrail.lua) and a 20-stage fading plasma tail.
local function CannonTrail(wd)
	if wd.cegtag == nil then
		wd.cegtag = "plasmacannontrail"
	end
	if wd.stages == nil then
		wd.stages = 20
		wd.alphadecay = 1 - ((1 / wd.stages) / 1.5)
		wd.sizedecay = 0.4 / wd.stages
		wd.separation = 1
	end
end

function WeaponDef_Post(name, weaponDef)
	for i = 1, #TA_ONLY_TAGS do weaponDef[TA_ONLY_TAGS[i]] = nil end

	
	weaponDef.soundhitwet = ""
	if weaponDef.range and tonumber(weaponDef.range) < 550 or 
		weaponDef.reloadtime and tonumber(weaponDef.reloadtime)<1.5 or
		explosiveWeapons[weaponDef.weapontype] then
			weaponDef.avoidfeature = false	-- don't avoid features if short range, explosive or rapid fire weapon
	end
	if explosiveWeapons[weaponDef.weapontype] then
		-- (BOTA widened the area of effect of every explosive weapon with an edgeeffectiveness here; TA's AoE is used as is.)
		if weaponDef.weapontype == "Cannon" then
			weaponDef.size = CannonSize(weaponDef)
		end
		if weaponDef.weapontype == "Cannon" and weaponDef.range and not weaponDef.mygravity and not weaponDef.cylindertargeting and name:find("armsfig_weapon") == nil then -- exclude arm tornado weapon, because it fires cannon weapon type from the air down on land
			weaponDef.mygravity = TA_GRAVITY
			weaponDef.gravityaffected = true
		elseif weaponDef.interceptor then
			weaponDef.interceptor = interceptorStyle
		end
		if weaponDef.weapontype == "TorpedoLauncher" then
			weaponDef.soundhitwet = weaponDef.soundhitdry
			-- A dropped torpedo enters the water at plane speed (~11 elmos/frame, 3x its rated speed) and the engine never slows it,
			-- while it turns a fixed angle per frame: it needs 75 elmos (turnrate 15000) to over 150 (10000) to level off, and
			-- blows up on any shallower seabed. Touching the seabed instead sheds the excess speed and lets it steer on.
			weaponDef.groundbounce = true
			weaponDef.bouncerebound = 0.2
			weaponDef.bounceslip = 0.3
			weaponDef.numbounce = 2
		else
			local AoE = tonumber(weaponDef.areaofeffect) or 0
			if AoE<50 then
				weaponDef.soundhitwet = "splshbig"
			elseif AoE<88 then
				weaponDef.soundhitwet = "splssml"
			elseif AoE<145 then
				weaponDef.soundhitwet = "splsmed"
			elseif AoE>450 then
				weaponDef.soundhitwet = weaponDef.soundhitdry
			else
				weaponDef.soundhitwet = "splslrg"
			end
		end
	elseif inertialessWeapons[weaponDef.weapontype] then
		if weaponDef.weapontype == "LaserCannon" then
			LaserLook(weaponDef)
		end
		weaponDef.impulseboost = 0
		weaponDef.impulsefactor = 0
		weaponDef.soundhitwet = "sizzle"		
		if weaponDef.weapontype == "LaserCannon" or weaponDef.weapontype == "EmgCannon" then
			weaponDef.cegtag = ""	-- we use the projectile lights widget now
		elseif weaponDef.weapontype == "BeamLaser" then
			weaponDef.soundhitdry = ""
			weaponDef.soundtrigger = 1
			--weaponDef.sweepfire = 0	-- at least till test phase of spring is over
		elseif weaponDef.weapontype == "DGun" then
			weaponDef.waterweapon = true	-- make DGun ball pierce water, but don't allow firing while under water
			weaponDef.firesubmersed = false
			weaponDef.avoidFriendly = false	-- make DGun ball shoot through anything, anywhere, anytime
			weaponDef.avoidFeature = false
			weaponDef.avoidGround = false
			weaponDef.avoidNeutral = false
		end
	end	
	if weaponDef.cratermult then 
		weaponDef.cratermult = weaponDef.cratermult * 0.4
	else
		weaponDef.cratermult = 0.4
	end
	if weaponDef.craterboost then
		weaponDef.craterboost = weaponDef.craterboost * 0.4
	else
		weaponDef.craterboost = 0
	end

	if weaponDef.weapontype == "Cannon" then
		CannonTrail(weaponDef)
	end

	-- Don't collide with friendlies (modoption)
	if modOptions.nocollide and tobool(modOptions.nocollide) then
		weaponDef.collidefriendly = false
	end
end
