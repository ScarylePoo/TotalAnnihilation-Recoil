-- Freaker (CORE_T2_BOT_Freaker): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Freaker.COB: aiming queues RequestState(0) -> activatescr (arms come up, the gun arm
-- swings forward) and turns the torso at 250 deg/s; after the restore delay (reload * 2) RequestState(1) ->
-- deactivatescr and the torso returns at 150 deg/s. Each shot snaps the right forearm to -50 deg like the COB. Fires
-- from Flare, aims from the torso, same death table and corpse types (old Hip/LULeg/LLLeg map to the skeleton).
-- Keyframes are the COB's (move-x / turn-z sign-flipped, zero-speed no-ops dropped, the old legs' resets dropped).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
gp, torso, thrust, head, luarm, llarm, flare, ruarm, rlarm =
	piece('gp', 'torso', 'thrust', 'head', 'luarm', 'llarm', 'flare', 'ruarm', 'rlarm')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 3000

local function activatescr()
	Move(torso, y_axis, 0)
	Move(thrust, z_axis, 0)
	Move(luarm, x_axis, 0)
	Move(ruarm, x_axis, 0)
	Move(llarm, y_axis, 0)
	Move(flare, x_axis, -0.351)
	Move(flare, y_axis, 3.209)
	Move(flare, z_axis, -0.25)
	Turn(luarm, x_axis, rad(0))
	Turn(luarm, x_axis, rad(-9.84), rad(34.41))
	Turn(ruarm, z_axis, rad(0))
	Turn(rlarm, x_axis, rad(0))
	Turn(rlarm, x_axis, rad(-11.95), rad(41.79))
	Turn(llarm, x_axis, rad(0))
	Turn(llarm, x_axis, rad(-32.34), rad(113.09))
	Sleep(286)
	Turn(luarm, x_axis, rad(-17.23), rad(25.28))
	Turn(ruarm, y_axis, rad(-11.25), rad(38.52))
	Turn(rlarm, x_axis, rad(-35.51), rad(80.66))
	Turn(llarm, x_axis, rad(-68.2), rad(122.81))
	Sleep(292)
	Sleep(11)
end

local function deactivatescr()
	Move(torso, y_axis, 0)
	Move(thrust, z_axis, 0)
	Move(luarm, x_axis, 0)
	Move(ruarm, x_axis, 0)
	Move(rlarm, y_axis, 0)
	Move(llarm, y_axis, 0)
	Move(flare, x_axis, -0.351)
	Move(flare, y_axis, 3.209)
	Move(flare, z_axis, -0.25)
	Turn(luarm, x_axis, rad(-17.23))
	Turn(luarm, x_axis, rad(-9.84), rad(45.02))
	Turn(ruarm, y_axis, rad(-11.25))
	Turn(ruarm, y_axis, rad(0), rad(68.59))
	Turn(ruarm, z_axis, rad(0))
	Turn(rlarm, x_axis, rad(-35.51))
	Turn(rlarm, x_axis, rad(-11.95), rad(143.62))
	Turn(llarm, x_axis, rad(-68.2))
	Turn(llarm, x_axis, rad(-32.34), rad(218.65))
	Sleep(164)
	Turn(luarm, x_axis, rad(0), rad(59.66))
	Turn(rlarm, x_axis, rad(0), rad(72.44))
	Turn(llarm, x_axis, rad(0), rad(196.02))
	Sleep(165)
	Sleep(6)
end
-- COB RequestState: one worker runs the scripts until the requested state stops changing (0 = up, 1 = down)
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then activatescr() else deactivatescr() end
	end
	busy = false
end

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	StartThread(RequestState, 1)
	Turn(torso, y_axis, 0, rad(150))
	WaitForTurn(torso, y_axis)
end

function script.AimWeapon(num, heading, pitch)
	StartThread(RequestState, 0)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(250))
	WaitForTurn(torso, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.FireWeapon(num)
	Turn(rlarm, x_axis, rad(-50))
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return flare                  -- COB: piece 1
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({head, pelvis, llarm, lleg, luarm, lthigh, rlarm, rleg, ruarm, rthigh, thrust, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({head, pelvis, llarm, lleg, luarm, lthigh, rlarm, rleg, ruarm, rthigh, thrust}, SFX.FALL)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({head, pelvis, llarm, lleg, luarm, lthigh, rlarm, rleg, ruarm, rthigh, thrust}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 2
	end
	Blow({head, pelvis, llarm, lleg, luarm, lthigh, rlarm, rleg, ruarm, rthigh, thrust}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
