-- Hurricane: heavy bomber with a retractable belly gun and a dorsal V-tail (hand port of the COB, deliberately not faithful:
-- the OTA model carried the gun on top and the tail plates below). Weapon 1 = bombs, weapon 2 = twin laser.
include "smokeunit.lua"

local base, bombs, turret, barrels, flare1, flare2 = piece('base', 'bombs', 'turret', 'barrels', 'flare1', 'flare2')
local wing1, wing2, tail1, tail2, thrusta1, thrusta2 = piece('wing1', 'wing2', 'tail1', 'tail2', 'thrusta1', 'thrusta2')

local SIG_AIM_LASER = 2

local rad = math.rad
local FOLD_SPEED = rad(75.63)
local WING_OUT = rad(90)
local TAIL_SPEED = rad(25.41)
local TAIL_RISE = rad(30.23)

-- The turret's rest position is inside the fuselage (aircraft sit with y = 0 on the ground). It comes down once the plane is well off the
-- ground and goes back up on the way down. Done on altitude and not in Activate/Deactivate because, measured in the engine, Deactivate
-- only comes about 30 elmos up and the plane is sinking 3 elmos a frame by then: 10 frames from touchdown. Straightening the barrels and
-- raising the gun takes about 20 frames, plus the 13.4 elmos they reach below the unit when pointing straight down.
local GUN_DROP = 6.0             -- matches the spec's GUN_DROP
local GUN_SPEED = 15.0
local GUN_DOWN_AT = 130          -- elmos above ground to lower
local GUN_UP_AT = 100            -- ... and to retract
local gunDown = false
local laserMuzzle = flare1

local function RestoreGun()
	SetSignalMask(SIG_AIM_LASER)
	Sleep(3000)
	Turn(turret, y_axis, 0, rad(90))
	Turn(barrels, x_axis, 0, rad(50))
end

local function GunGear()
	while true do
		local x, y, z = Spring.GetUnitPosition(unitID)
		local height = y - math.max(Spring.GetGroundHeight(x, z), 0)
		if gunDown and height < GUN_UP_AT then
			gunDown = false
			Signal(SIG_AIM_LASER)
			Turn(turret, y_axis, 0, rad(390))
			Turn(barrels, x_axis, 0, rad(350))
			WaitForTurn(barrels, x_axis)
			WaitForTurn(turret, y_axis)
			Move(turret, y_axis, 0, GUN_SPEED)
			WaitForMove(turret, y_axis)
		elseif not gunDown and height > GUN_DOWN_AT then
			Move(turret, y_axis, -GUN_DROP, GUN_SPEED)
			WaitForMove(turret, y_axis)
			gunDown = true
		end
		Sleep(100)
	end
end

function script.Create()
	StartThread(SmokeUnit, {thrusta1, thrusta2})
	StartThread(GunGear)
end

function script.Activate()
	Turn(wing1, z_axis, WING_OUT, FOLD_SPEED)
	Turn(wing2, z_axis, -WING_OUT, FOLD_SPEED)
	Turn(tail1, z_axis, -TAIL_RISE, TAIL_SPEED)
	Turn(tail2, z_axis, TAIL_RISE, TAIL_SPEED)
end

function script.Deactivate()
	Turn(wing1, z_axis, 0, FOLD_SPEED)
	Turn(wing2, z_axis, 0, FOLD_SPEED)
	Turn(tail1, z_axis, 0, TAIL_SPEED)
	Turn(tail2, z_axis, 0, TAIL_SPEED)
end

-- bombs: free-fall from the bay, nothing to aim
function script.AimWeapon1(heading, pitch)
	return true
end

function script.AimFromWeapon1()
	return bombs
end

function script.QueryWeapon1()
	return bombs
end

function script.AimWeapon2(heading, pitch)
	Signal(SIG_AIM_LASER)
	SetSignalMask(SIG_AIM_LASER)
	if not gunDown then return false end
	Turn(turret, y_axis, heading, rad(390))
	Turn(barrels, x_axis, -pitch, rad(350))
	WaitForTurn(turret, y_axis)
	WaitForTurn(barrels, x_axis)
	StartThread(RestoreGun)
	return true
end

function script.AimFromWeapon2()
	return barrels
end

function script.QueryWeapon2()
	return laserMuzzle
end

function script.FireWeapon2()
	laserMuzzle = (laserMuzzle == flare1) and flare2 or flare1
end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth
	local burn = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE

	if severity <= 0.25 then
		Explode(barrels, SFX.NONE)
		Explode(base, SFX.NONE)
		Explode(tail1, SFX.NONE)
		Explode(tail2, SFX.NONE)
		Explode(turret, SFX.NONE)
		Explode(wing1, SFX.NONE)
		Explode(wing2, SFX.NONE)
		return 1                -- leave a wreck

	elseif severity <= 0.50 then
		Explode(barrels, SFX.FALL)
		Explode(base, SFX.NONE)
		Explode(tail1, SFX.FALL)
		Explode(tail2, SFX.FALL)
		Explode(turret, SFX.FALL)
		Explode(wing1, SFX.SHATTER)
		Explode(wing2, SFX.NONE)
		return 2                -- leave a heap

	else
		Explode(barrels, burn)
		Explode(base, SFX.NONE)
		Explode(tail1, burn)
		Explode(tail2, burn)
		Explode(turret, burn)
		Explode(wing1, SFX.SHATTER)
		Explode(wing2, SFX.NONE)
		return 3                -- leave nothing
	end
end
