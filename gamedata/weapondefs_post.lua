--------------------------------------------------------------------------------
-- Weapon Definitions Post-processing
--------------------------------------------------------------------------------
local pairs = pairs
local math = math


local function tobool(val)
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

-- Weapons/*.lua use native Recoil tags (weapontype, rgbcolor, gravityaffected,
-- craterareaofeffect...). The TA tags (rendertype, lineofsight, ballistic,
-- color...) were converted with springcontent's weapondefs_post.lua once and
-- removed, so neither that conversion nor a TA-tag strip runs here any more.


--------------------------------------------------------------------------------
-- BOTA Weapon Definitions Post-processing
--------------------------------------------------------------------------------
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

local modOptions = Spring.GetModOptions()

-- Adjustment of terrain damage, area of effect, kinetic force of weapons and cannon trajectory height
local customGravity = 0.25
local maxRangeAngle = 30  --in degrees >0 and <=45
if modOptions and modOptions.gravity then customGravity=modOptions.gravity end
local velGravFactor = customGravity * 900 / math.sin(math.rad(2 * maxRangeAngle))
local interceptorStyle = 2
if modOptions and modOptions.nuke and not tobool(modOptions.nuke) then interceptorStyle = 1 end

for id, weaponDef in pairs(WeaponDefs) do
	
	weaponDef.soundhitwet = ""
	if weaponDef.range and tonumber(weaponDef.range) < 550 or 
		weaponDef.reloadtime and tonumber(weaponDef.reloadtime)<1.5 or
		explosiveWeapons[weaponDef.weapontype] then
			weaponDef.avoidfeature = false	-- don't avoid features if short range, explosive or rapid fire weapon
	end
	if explosiveWeapons[weaponDef.weapontype] then
		if weaponDef.edgeeffectiveness and tonumber(weaponDef.edgeeffectiveness)>0 and tonumber(weaponDef.areaofeffect)<145 then
			weaponDef.areaofeffect = math.min(weaponDef.areaofeffect / (1 - weaponDef.edgeeffectiveness), 160)
			weaponDef.edgeeffectiveness = 0
		end
		if weaponDef.weapontype == "Cannon" and weaponDef.range and not weaponDef.mygravity and not weaponDef.cylindertargeting and id:find("armsfig_weapon") == nil then -- exclude arm tornado weapon, because it fires cannon weapon type from the air down on land
			weaponDef.mygravity = customGravity
			weaponDef.weaponvelocity = math.sqrt(weaponDef.range * velGravFactor)
			weaponDef.gravityaffected = true
			weaponDef.heightboostfactor = 0.04
		elseif weaponDef.interceptor then
			weaponDef.interceptor = interceptorStyle
		end
		if weaponDef.weapontype == "TorpedoLauncher" then
			weaponDef.soundhitwet = weaponDef.soundhitdry
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
end

--------------------------------------------------------------------------------
-- Don't Collide with friendlies for all weapons

if (modOptions.nocollide and tobool(modOptions.nocollide)) then
	for id in pairs(WeaponDefs) do
		WeaponDefs[id].collidefriendly = false
	end
end