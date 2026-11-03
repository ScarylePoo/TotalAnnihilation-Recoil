-- Arm Commander (ARM_Commander, unit key arm_commander): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's scripts/arm_commander.cob. The unit def names this file with script = "ARM_Commander.lua"; the stock
-- unit_script gadget lowercases that name and the VFS is case-insensitive.
-- COB logic kept: the laser (AimPrimary, weapon 1) turns the torso at 300 deg/s and raises the left (lathe/laser) arm to
-- -pitch - 30 deg at 90 deg/s, fires from lfirept, and refuses to aim while the D-gun holds the unit (COB static 3). The D-gun
-- (AimTertiary, weapon 3) raises the right arm to -pitch - 24 deg at 90 deg/s, aims from pelvis and fires from rbigflash.
-- Building, repairing, reclaiming and capturing all reach StartBuilding: the lathe arm aims like the laser, then
-- INBUILDSTANCE is set; nano spray from nanospray. RestorePosition: torso 90 deg/s, arms 45 deg/s, on StopBuilding.
-- Not in the COB: the elbows. The COB's arms only looked right because its walk left the forearms bent; this model's arms hang straight
-- down (-Y), so the aim also bends the forearm to complete 90 deg, and the barrel ends up on -pitch. Measured with zz_commander_aim_probe.
-- An aim during a build returns to the build stance afterwards rather than lowering the arm.
-- Replaced: TargetCleared is COB-only, so RestorePosition also runs after a delay (laser reload * 2) following an aim.
-- Dropped: the old walk and MotionControl (scripts/headers/walk.lua walks now; the COB's wait for its walk frame to end is
-- gone with it), the flare show/hide (the flare pieces are empty).
-- Nothing else to port: the COB has no cloak, reclaim or capture callin (the engine does those from the unit def), no smoke,
-- no Killed. Commanders have no corpse; death and self-destruct are the def's COMMANDER_EXPLOSION.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, head, ruparm, biggun, rbigflash = piece('ground', 'torso', 'head', 'ruparm', 'biggun', 'rbigflash')
luparm, nanolath, lfirept, nanospray = piece('luparm', 'nanolath', 'lfirept', 'nanospray')

local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local TORSO_AIM, ARM_AIM = rad(299.93), rad(89.98)
local ELBOW_AIM, ELBOW_REST = rad(179.96), rad(89.98)
local LASER_UP, LASER_ELBOW = rad(29.99), rad(-60.01)   -- upper arm + forearm = 90 deg: hanging -> level
local DGUN_UP, DGUN_ELBOW = rad(23.99), rad(-66.01)
local buildHeading, buildPitch                          -- set while building
local restoreDelay = 3000
local bigGunAimed = false     -- COB static 3

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = math.max(1000, WeaponDefs[wd.weaponDef].reload * 2000)
	end
end

local function RestorePosition()
	bigGunAimed = false
	Turn(torso, y_axis, 0, rad(89.98))
	Turn(ruparm, x_axis, 0, rad(44.99))
	Turn(luparm, x_axis, 0, rad(44.99))
	Turn(biggun, x_axis, 0, ELBOW_REST)
	Turn(nanolath, x_axis, 0, ELBOW_REST)
	WaitForTurn(torso, y_axis)
	WaitForTurn(ruparm, x_axis)
	WaitForTurn(luparm, x_axis)
end

local function BuildPose(heading, pitch)
	Turn(torso, y_axis, heading, TORSO_AIM)
	Turn(luparm, x_axis, -pitch - LASER_UP, ARM_AIM)
	Turn(nanolath, x_axis, LASER_ELBOW, ELBOW_AIM)
	WaitForTurn(torso, y_axis)
	WaitForTurn(luparm, x_axis)
	WaitForTurn(nanolath, x_axis)
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	if buildHeading then
		bigGunAimed = false
		Turn(ruparm, x_axis, 0, rad(44.99))
		Turn(biggun, x_axis, 0, ELBOW_REST)
		BuildPose(buildHeading, buildPitch)
	else
		RestorePosition()
	end
end

function script.AimWeapon(num, heading, pitch)
	if num ~= 3 and bigGunAimed then return false end
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, TORSO_AIM)
	if num == 3 then
		bigGunAimed = true
		Turn(ruparm, x_axis, -pitch - DGUN_UP, ARM_AIM)
		Turn(biggun, x_axis, DGUN_ELBOW, ELBOW_AIM)
		WaitForTurn(torso, y_axis)
		WaitForTurn(ruparm, x_axis)
		WaitForTurn(biggun, x_axis)
	else
		Turn(luparm, x_axis, -pitch - LASER_UP, ARM_AIM)
		Turn(nanolath, x_axis, LASER_ELBOW, ELBOW_AIM)
		WaitForTurn(torso, y_axis)
		WaitForTurn(luparm, x_axis)
		WaitForTurn(nanolath, x_axis)
	end
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return (num == 3) and pelvis or torso           -- COB: pieces 5 / 0
end

function script.QueryWeapon(num)
	return (num == 3) and rbigflash or lfirept      -- COB: pieces 3 / 6
end

function script.FireWeapon(num)
end

-- COB StartBuilding sets no signal mask: an aim does not cancel it, so the build stance is always reached
local function BuildAim(heading, pitch)
	BuildPose(heading, pitch)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

function script.StartBuilding(heading, pitch)
	buildHeading, buildPitch = heading, pitch
	StartThread(BuildAim, heading, pitch)
end

local function StopBuild()
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	RestorePosition()
end

function script.StopBuilding()
	buildHeading, buildPitch = nil, nil
	SetUnitValue(COB.INBUILDSTANCE, 0)
	StartThread(StopBuild)
end

function script.QueryNanoPiece()
	return nanospray              -- COB: piece 4
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

function script.Killed(recentDamage, maxHealth)
	return 1
end
