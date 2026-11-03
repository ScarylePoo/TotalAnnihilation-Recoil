-- Decoy Commander (CORE_T2_BOT_DecoyCommander): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_DecoyCommander.COB (same layout as the Core Commander's): the laser (weapon 4) turns
-- the chest at 300 deg/s unless the D-gun holds it and raises the left arm (l_sho x -pitch at 180 deg/s; the COB's extra -30 deg aimed this forward-pointing gauntlet 30 deg high),
-- fires from mlasflsh and relaxes after 2 s; weapon 3 (the D-gun slot) aims r_dgun the same way, fires from bigflsh
-- with the COB's BigFire recoil keyframes. Building aims the left arm and sets INBUILDSTANCE; nano spray from
-- nanospray. AmphSpeed: max speed rises with water depth (x1 at the surface to x2 at 25 elmo deep) as in the COB.
-- The COB has no Killed: the wreck is always left (corpse 1). The old walk is replaced by the shared one.
-- No damage smoke: neither the COB nor the real commander has any, and it would give the decoy away.
-- COB move-x / turn-z values are sign-flipped (Recoil CobInstance.h "COBWTF").

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, chest, head, l_sho, l_nano, mlasflsh, nanospray, r_sho, r_dgun, bigflsh =
	piece('ground', 'chest', 'head', 'l_sho', 'l_nano', 'mlasflsh', 'nanospray', 'r_sho', 'r_dgun', 'bigflsh')

local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_LASER, SIG_DGUN = 2, 4
local MAX_SPEED = COB.MAX_SPEED or 75
local laserAimed, dgunAimed = false, false   -- COB statics 1 / 2

local function BigFire()
	Move(r_sho, z_axis, 0)
	Move(r_sho, z_axis, -7.5, 625)
	Move(r_dgun, z_axis, 0)
	Move(r_dgun, z_axis, -12.5, 1300)
	Move(bigflsh, x_axis, 0)
	Move(mlasflsh, y_axis, 0)
	Move(mlasflsh, z_axis, 0)
	Turn(r_sho, x_axis, rad(0))
	Turn(r_sho, x_axis, rad(-1), rad(112.97))
	Sleep(10)
	Move(r_sho, z_axis, -2.5, 40)
	Move(r_dgun, z_axis, -7.5, 75)
	Turn(r_sho, x_axis, rad(0), rad(14))
	Sleep(80)
	Move(r_sho, z_axis, 0, 35)
	Move(r_dgun, z_axis, -5, 37.5)
	Sleep(70)
	Move(r_sho, z_axis, 0, 2.5)
	Turn(r_sho, x_axis, rad(1), rad(15))
	Turn(r_sho, z_axis, rad(0), rad(8))
	Sleep(50)
	Move(r_sho, z_axis, 0, 12.5)
	Move(r_dgun, z_axis, 0, 110)
	Turn(r_sho, x_axis, rad(0), rad(19))
	Turn(r_sho, z_axis, rad(0), rad(9))
	Sleep(40)
	Sleep(10)
end
local function AmphSpeed()
	local base = GetUnitValue(MAX_SPEED)
	while true do
		local _, y = Spring.GetUnitBasePosition(unitID)
		y = y or 0
		if y >= 0 then
			SetUnitValue(MAX_SPEED, base)
		elseif y < -25 then
			SetUnitValue(MAX_SPEED, base * 2)
		else
			SetUnitValue(MAX_SPEED, math.floor(base * (1 - y / 25)))
		end
		Sleep(30)
	end
end

function script.Create()
	Hide(ground)
	StartThread(AmphSpeed)
end

local function RestoreLaser()
	Sleep(2000)
	laserAimed = false
	Turn(l_sho, x_axis, 0, rad(179.96))
	if not dgunAimed then Turn(chest, y_axis, 0, rad(299.93)) end
end

local function RestoreDgun()
	SetSignalMask(SIG_DGUN)
	Sleep(2000)
	dgunAimed = false
	Turn(r_dgun, x_axis, 0, rad(179.96))
	if not laserAimed then Turn(chest, y_axis, 0, rad(299.93)) end
end

function script.AimWeapon(num, heading, pitch)
	if num == 3 then
		Signal(SIG_DGUN)
		SetSignalMask(SIG_DGUN)
		dgunAimed = true
		Turn(chest, y_axis, heading, rad(299.93))
		Turn(r_dgun, x_axis, -pitch, rad(179.96))
		WaitForTurn(chest, y_axis)
		WaitForTurn(r_dgun, x_axis)
		StartThread(RestoreDgun)
		return true
	end
	Signal(SIG_LASER)
	SetSignalMask(SIG_LASER)
	laserAimed = true
	if not dgunAimed then
		Turn(chest, y_axis, heading, rad(299.93))
		Turn(l_sho, x_axis, -pitch, rad(179.96))
		WaitForTurn(l_sho, x_axis)
	end
	StartThread(RestoreLaser)
	return true
end

function script.AimFromWeapon(num)
	return chest                  -- COB: piece 1
end

function script.QueryWeapon(num)
	return (num == 3) and bigflsh or mlasflsh       -- COB: pieces 3 / 2
end

function script.FireWeapon(num)
	if num == 3 then StartThread(BigFire) end
end

function script.StartBuilding(heading, pitch)
	if not laserAimed then
		Turn(l_sho, x_axis, -pitch, rad(179.96))
		if not dgunAimed then Turn(chest, y_axis, heading, rad(299.93)) end
	end
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

function script.StopBuilding()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	if not laserAimed then Turn(l_sho, x_axis, 0, rad(179.96)) end
	if not laserAimed and not dgunAimed then Turn(chest, y_axis, 0, rad(299.93)) end
end

function script.QueryNanoPiece()
	return nanospray              -- COB: piece 4
end

function script.SweetSpot(num)
	return chest                  -- COB: piece 1
end

function script.Killed(recentDamage, maxHealth)
	return 1
end
