function gadget:GetInfo()
	return {
		name    = "Muzzle Flashes",
		desc    = "Spawns each weapon's muzzle flash CEG (customparams.muzzleceg) where its shot is created",
		author  = "TA:Recoil",
		license = "GPL v2 or later",
		layer   = 0,
		enabled = true,
	}
end

-- One gadget instead of EmitSfx calls in ~250 unit scripts (COB and Lua): every projectile starts at the firing
-- piece, travelling the way the barrel points, so the flash goes there. The effect per weapon is chosen in
-- gamedata/alldefs_post.lua (MuzzleCEG); the effects are gamedata/explosions/tar-muzzleflashes.lua.

if not gadgetHandler:IsSyncedCode() then
	return
end

local GetProjectilePosition  = Spring.GetProjectilePosition
local GetProjectileVelocity  = Spring.GetProjectileVelocity
local GetProjectileDirection = Spring.GetProjectileDirection
local SpawnCEG = Spring.SpawnCEG
local sqrt = math.sqrt

local muzzle = {}

function gadget:Initialize()
	local watch = Script.SetWatchProjectile or Script.SetWatchWeapon
	for weaponDefID, wd in pairs(WeaponDefs) do
		local ceg = wd.customParams and wd.customParams.muzzleceg
		if ceg and ceg ~= "" then
			muzzle[weaponDefID] = ceg
			watch(weaponDefID, true)
		end
	end
end

function gadget:ProjectileCreated(proID, ownerID, weaponDefID)
	local ceg = muzzle[weaponDefID]
	if not ceg then
		return
	end
	local x, y, z = GetProjectilePosition(proID)
	if not x then
		return
	end
	local dx, dy, dz
	if GetProjectileDirection then
		dx, dy, dz = GetProjectileDirection(proID)
	end
	if not dx or (dx == 0 and dy == 0 and dz == 0) then
		local vx, vy, vz = GetProjectileVelocity(proID)
		local l = vx and sqrt(vx * vx + vy * vy + vz * vz) or 0
		if l > 0 then
			dx, dy, dz = vx / l, vy / l, vz / l
		else
			dx, dy, dz = 0, 1, 0
		end
	end
	SpawnCEG(ceg, x, y, z, dx, dy, dz)
end
