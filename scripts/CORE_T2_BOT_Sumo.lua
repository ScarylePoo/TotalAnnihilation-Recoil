-- Sumo (CORE_T2_BOT_Sumo): Lua unit script for the remodelled TRACKED Sumo (user's decision: tracks, not legs).
-- Ported from TA's CORE_T2_BOT_Sumo.COB without its walk: the turret turns at 140 deg/s and both cannons pitch at
-- 35 deg/s; after the restore delay (reload * 2) the turret returns at 90 and the guns at 45 deg/s. Shots alternate
-- rflare/lflare with the COB's barrel kick (-5 elmo, back at 10 elmo/s); aims from the turret, SweetSpot = body;
-- the death table and corpse types are the COB's minus the removed feet. New: the tracked hull's four frame pieces
-- (tracks1..4) are cycled while moving to run the treads.

hips, body, knobs, turret, faceguard = piece('hips', 'body', 'knobs', 'turret', 'faceguard')
lgun, lbarrel, lflare, rgun, rbarrel, rflare = piece('lgun', 'lbarrel', 'lflare', 'rgun', 'rbarrel', 'rflare')
rightchunk, leftchunk = piece('rightchunk', 'leftchunk')
local TRACKS = {piece('tracks1', 'tracks2', 'tracks3', 'tracks4')}

include "smokeunit.lua"

local rad = math.rad
local SIG_MOVE, SIG_AIM = 2, 4
local restoreDelay = 3000
local gun = 0                 -- COB static 4: 0 = right fires next

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
	StartThread(SmokeUnit, {body})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(turret, y_axis, 0, rad(90))
	Turn(rgun, x_axis, 0, rad(45))
	Turn(lgun, x_axis, 0, rad(45))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(turret, y_axis, heading, rad(140))
	Turn(rgun, x_axis, -pitch, rad(35))
	Turn(lgun, x_axis, -pitch, rad(35))
	WaitForTurn(turret, y_axis)
	WaitForTurn(rgun, x_axis)
	WaitForTurn(lgun, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

local function Kick(barrel)
	Move(barrel, z_axis, -5)
	Sleep(150)
	Move(barrel, z_axis, 0, 10)
end

function script.FireWeapon(num)
	StartThread(Kick, (gun == 0) and rbarrel or lbarrel)
	gun = 1 - gun
end

function script.AimFromWeapon(num)
	return turret                 -- COB: piece 3
end

function script.QueryWeapon(num)
	return (gun == 0) and rflare or lflare          -- COB: pieces 0 / 1
end

function script.SweetSpot(num)
	return body                   -- COB: piece 2
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({body, knobs, lbarrel, leftchunk, lflare, lgun, rbarrel, rflare, rgun, rightchunk, turret}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({body, leftchunk, rightchunk}, SFX.NONE)
		Blow({knobs, lbarrel, lflare, lgun, rbarrel, rflare, rgun, turret}, SFX.FALL)
		return 2
	elseif severity <= 99 then
		Blow({body}, SFX.SHATTER)
		Blow({knobs, lbarrel, lflare, lgun, rbarrel, rflare, rgun, turret}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({leftchunk, rightchunk}, SFX.NONE)
		return 3
	end
	Blow({body}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	Blow({knobs, lbarrel, lflare, lgun, rbarrel, rflare, rgun, turret}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({leftchunk, rightchunk}, SFX.NONE)
	return 3
end
