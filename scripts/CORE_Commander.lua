-- Core Commander (CORE_Commander, unit key core_commander): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's scripts/core_commander.cob. The unit def names this file with script = "CORE_Commander.lua"; the stock
-- unit_script gadget lowercases that name and the VFS is case-insensitive.
-- COB logic kept: the laser (AimPrimary, weapon 1) turns the chest at 300 deg/s and raises the left arm (l_sho) to
-- -pitch - 30 deg at 90 deg/s, aims from chest, fires from mlasflsh, and refuses to aim while the D-gun holds the unit (COB
-- static 3). The D-gun (AimTertiary, weapon 3) aims r_dgun to -pitch at 150 deg/s, aims from r_dgun, fires from bigflsh, and
-- after 100 ms plays BigFire (the recoil keyframes). Building, repairing, reclaiming and capturing all reach StartBuilding: it
-- cancels aims (shared signal), aims the left arm like the laser, sets INBUILDSTANCE. The nano spray comes from mlasflsh:
-- the COB's QueryNanoPiece returns piece 1, not nanospray (the COB only ever moves nanospray, in frames that are gone).
-- Replaced: TargetCleared is COB-only, so RestorePosition also runs after a delay (laser reload * 2) following an aim. It now
-- lowers both arms too: the COB's RestorePosition only turned the chest and left that to the old walk's arm swing.
-- Dropped: the old walk, stand and MotionControl (scripts/headers/walk.lua walks now; the COB's wait for its walk frame to
-- end is gone with it), the flare show/hide (the flare pieces are empty), the no-op moves of bigflsh and mlasflsh by 0.
-- No COB z-turn or x-move has a non-zero value, so the COB -> Lua sign flips change nothing here.
-- Nothing else to port: the COB has no cloak, reclaim or capture callin (the engine does those from the unit def), no smoke,
-- no Killed. Commanders have no corpse; death and self-destruct are the def's COMMANDER_EXPLOSION.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, chest, head, l_sho, l_nano, mlasflsh, nanospray, r_sho, r_dgun, bigflsh =
	piece('ground', 'chest', 'head', 'l_sho', 'l_nano', 'mlasflsh', 'nanospray', 'r_sho', 'r_dgun', 'bigflsh')

local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local CHEST_AIM, LASER_ARM, DGUN_ARM = rad(299.93), rad(89.98), rad(149.96)
local restoreDelay = 3000
local dgunAimed = false       -- COB static 3

local function BigFire()
	Sleep(100)                -- COB FireTertiary: the flare frame before the recoil
	Move(r_sho, z_axis, 0)
	Move(r_sho, z_axis, -7.5, 625)
	Move(r_dgun, z_axis, 0)
	Move(r_dgun, z_axis, -12.5, 1300)
	Turn(r_sho, x_axis, 0)
	Turn(r_sho, x_axis, rad(-1), rad(112.97))
	Sleep(10)
	Move(r_sho, z_axis, -2.5, 40)
	Move(r_dgun, z_axis, -7.5, 75)
	Turn(r_sho, x_axis, 0, rad(14))
	Sleep(80)
	Move(r_sho, z_axis, 0, 35)
	Move(r_dgun, z_axis, -5, 37.5)
	Sleep(70)
	Move(r_sho, z_axis, 0, 2.5)
	Turn(r_sho, x_axis, rad(1), rad(15))
	Turn(r_sho, z_axis, 0, rad(8))
	Sleep(50)
	Move(r_sho, z_axis, 0, 12.5)
	Move(r_dgun, z_axis, 0, 110)
	Turn(r_sho, x_axis, 0, rad(19))
	Turn(r_sho, z_axis, 0, rad(9))
	Sleep(50)
end

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = math.max(1000, WeaponDefs[wd.weaponDef].reload * 2000)
	end
end

local function RestorePosition()
	dgunAimed = false
	Turn(chest, y_axis, 0, rad(89.98))
	Turn(l_sho, x_axis, 0, rad(44.99))
	Turn(r_dgun, x_axis, 0, rad(44.99))
	WaitForTurn(chest, y_axis)
	WaitForTurn(l_sho, x_axis)
	WaitForTurn(r_dgun, x_axis)
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	RestorePosition()
end

function script.AimWeapon(num, heading, pitch)
	if num ~= 3 and dgunAimed then return false end
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(chest, y_axis, heading, CHEST_AIM)
	if num == 3 then
		dgunAimed = true
		Turn(r_dgun, x_axis, -pitch, DGUN_ARM)
		WaitForTurn(chest, y_axis)
		WaitForTurn(r_dgun, x_axis)
	else
		Turn(l_sho, x_axis, -pitch - rad(29.99), LASER_ARM)
		WaitForTurn(chest, y_axis)
		WaitForTurn(l_sho, x_axis)
	end
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return (num == 3) and r_dgun or chest           -- COB: pieces 10 / 0
end

function script.QueryWeapon(num)
	return (num == 3) and bigflsh or mlasflsh       -- COB: pieces 2 / 1
end

function script.FireWeapon(num)
	if num == 3 then StartThread(BigFire) end
end

local function BuildAim(heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(chest, y_axis, heading, CHEST_AIM)
	Turn(l_sho, x_axis, -pitch - rad(29.99), LASER_ARM)
	WaitForTurn(chest, y_axis)
	WaitForTurn(l_sho, x_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

function script.StartBuilding(heading, pitch)
	StartThread(BuildAim, heading, pitch)
end

local function StopBuild()
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	RestorePosition()
end

function script.StopBuilding()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	StartThread(StopBuild)
end

function script.QueryNanoPiece()
	return mlasflsh               -- COB: piece 1
end

function script.SweetSpot(num)
	return chest                  -- COB: piece 0
end

function script.Killed(recentDamage, maxHealth)
	return 1
end
