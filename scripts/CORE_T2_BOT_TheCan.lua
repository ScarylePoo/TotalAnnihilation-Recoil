-- The Can (CORE_T2_BOT_TheCan): Lua unit script for the remodelled TRACKED Can (user's decision: tracks, not legs).
-- Ported from TA's CORE_T2_BOT_TheCan.COB without its walk: the turret (head) turns at 90 deg/s and the gun
-- pitches at 45 deg/s, both return after the restore delay (reload * 2); each shot kicks the gun back 3.75 elmo (62.5
-- elmo/s) and returns it at 3.75 elmo/s; aims from the head, fires from firept, SweetSpot = torso; the death table and
-- corpse types are the COB's minus the removed leg pieces. New: the tracked hull's four frame pieces (tracks1..4)
-- are cycled while moving to run the treads.

ground, pelvis, belly, torso, head, gun, firept = piece('ground', 'pelvis', 'belly', 'torso', 'head', 'gun', 'firept')
local TRACKS = {piece('tracks1', 'tracks2', 'tracks3', 'tracks4')}

include "smokeunit.lua"

local rad = math.rad
local SIG_MOVE, SIG_AIM = 2, 4
local restoreDelay = 3000

local function TrackAnim()
	Signal(SIG_MOVE)
	SetSignalMask(SIG_MOVE)
	local f = 1
	while true do
		Hide(TRACKS[f])
		f = f % 4 + 1
		Show(TRACKS[f])
		Sleep(90)
	end
end

function script.StartMoving()
	StartThread(TrackAnim)
end

function script.StopMoving()
	Signal(SIG_MOVE)
end

function script.Create()
	for i = 2, 4 do Hide(TRACKS[i]) end
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(head, y_axis, 0, rad(90))
	Turn(gun, x_axis, 0, rad(45))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(head, y_axis, heading, rad(90))
	Turn(gun, x_axis, -pitch, rad(45))
	WaitForTurn(head, y_axis)
	WaitForTurn(gun, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

local function Recoil()
	Move(gun, z_axis, -3.75, 62.5)
	WaitForMove(gun, z_axis)
	Move(gun, z_axis, 0, 3.75)
end

function script.FireWeapon(num)
	StartThread(Recoil)
end

function script.AimFromWeapon(num)
	return head                   -- COB: piece 1
end

function script.QueryWeapon(num)
	return firept                 -- COB: piece 2
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({belly, firept, ground, gun, head, pelvis, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({belly, torso}, SFX.NONE)
		Blow({firept, ground, gun, head, pelvis}, SFX.FALL)
		return 2
	elseif severity <= 99 then
		Blow({belly, torso}, SFX.NONE)
		Blow({firept, ground, gun, head, pelvis}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		return 3
	end
	Blow({belly, torso}, SFX.NONE)
	Blow({firept, ground, gun, head, pelvis}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	return 3
end
