-- Zeus (ARM_T2_BOT_Zeus): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Zeus.COB: the lightning gun rides on the back (backgun); the first aim plays the COB's
-- draw keyframes (right arm reaches over the shoulder, gun shown / backgun hidden at 400 ms), then the torso turns to
-- the heading and the gun pitches (both 90 deg/s); after the restore delay (reload * 2) the torso turns back and the
-- holster keyframes put the gun away again. Keyframes, timings, the busy/holstered state machine, aim/query pieces and
-- the death table are the COB's. COB negates turn-z and move-x values (Recoil CobInstance.h "COBWTF"), so the z turns
-- (lelbow, lloarm) are sign-flipped here. The old walk (and its arm swing that blocked aiming) is replaced by the
-- shared walk (scripts/headers/walk.lua); the arms now hold the COB's holstered pose while walking.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, backgun, ruparm, rloarm, gun, flash = piece('ground', 'torso', 'backgun', 'ruparm', 'rloarm', 'gun', 'flash')
luparm, lelbow, lloarm, lhand = piece('luparm', 'lelbow', 'lloarm', 'lhand')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local restoreDelay = 3000
local holstered = true        -- COB static 3
local busy = false            -- COB static 4: a draw/holster animation is running

-- keyframes: {sleep ms, {piece, axis, degrees} | {piece, axis, elmos, 'move'}, ...} (Lua signs)
local DRAW = {
	{80, {ruparm, x_axis, -17.93}, {luparm, x_axis, -36.56}, {lloarm, z_axis, -22.15}, {lhand, y_axis, -43.94}, {rloarm, x_axis, -67.85}},
	{70, {ruparm, x_axis, -56.60}, {rloarm, x_axis, -82.62}},
	{70, {ruparm, x_axis, -75.59}, {rloarm, x_axis, -92.11}},
	{70, {ruparm, x_axis, -103.00}, {rloarm, x_axis, -107.58}},
	{80, {ruparm, x_axis, -114.25}, {rloarm, x_axis, -123.40}},
	{70, {ruparm, x_axis, -136.41}, {rloarm, x_axis, -134.64}},
	{70, {rloarm, x_axis, -107.58}},
	{60, {luparm, z_axis, 0.625, 'move'}, {luparm, x_axis, -36.56}, {rloarm, x_axis, -78.39}},
	{50, {luparm, z_axis, 1.25, 'move'}, {luparm, x_axis, -54.49}, {lelbow, z_axis, -15.82}, {lloarm, z_axis, -20.74},
		{lhand, y_axis, 0}, {rloarm, x_axis, -56.60}},
	{40, {luparm, z_axis, 2.0, 'move'}, {ruparm, x_axis, -114.25}, {luparm, x_axis, -55.90}, {lelbow, z_axis, -21.09},
		{lloarm, z_axis, -35.86}, {rloarm, x_axis, -55.55}},
	{30, {luparm, z_axis, 4.0, 'move'}, {ruparm, x_axis, -78.75}, {luparm, x_axis, -59.41}, {lelbow, z_axis, -24.26},
		{lloarm, z_axis, -52.38}},
	{20, {luparm, z_axis, 4.375, 'move'}, {rloarm, y_axis, 3.125, 'move'}, {ruparm, x_axis, -48.52}, {luparm, x_axis, -61.88},
		{lelbow, z_axis, -48.87}, {lloarm, z_axis, -40.78}, {lhand, y_axis, 56.95}},
	{70, {luparm, z_axis, 4.25, 'move'}, {rloarm, y_axis, 3.75, 'move'}, {ruparm, x_axis, 2.81}, {luparm, x_axis, -44.30},
		{lelbow, z_axis, -44.65}, {lloarm, z_axis, -46.05}, {lhand, y_axis, 34.45}, {rloarm, x_axis, -95.27}},
}
local HOLSTER = {
	{100, {luparm, z_axis, 4.25, 'move'}, {rloarm, y_axis, 3.75, 'move'}, {ruparm, x_axis, 2.81}, {luparm, x_axis, -44.30},
		{lelbow, z_axis, -44.65}, {lloarm, z_axis, -46.05}, {lhand, y_axis, 34.45}, {rloarm, x_axis, -95.27}},
	{80, {luparm, z_axis, 4.125, 'move'}, {rloarm, y_axis, 0.75, 'move'}, {ruparm, x_axis, -28.48}, {luparm, x_axis, -61.17},
		{lelbow, z_axis, -34.45}, {lloarm, z_axis, -30.23}, {lhand, y_axis, 54.14}, {rloarm, x_axis, -91.05}},
	{80, {luparm, z_axis, 2.875, 'move'}, {rloarm, y_axis, 0.375, 'move'}, {ruparm, x_axis, -56.95}, {luparm, x_axis, -53.09},
		{lelbow, z_axis, -28.47}, {lloarm, z_axis, -29.88}, {lhand, y_axis, 14.77}},
	{70, {luparm, z_axis, 2.125, 'move'}, {ruparm, x_axis, -105.47}, {luparm, x_axis, -44.30}, {lelbow, z_axis, -24.61},
		{lhand, y_axis, -1.05}},
	{70, {ruparm, x_axis, -124.10}, {luparm, x_axis, -43.95}, {lelbow, z_axis, -17.92}, {lhand, y_axis, -8.44},
		{rloarm, x_axis, -112.50}},
	{130, {luparm, z_axis, 1.25, 'move'}, {ruparm, x_axis, -148.01}, {luparm, x_axis, -42.54}, {lelbow, z_axis, -15.81},
		{lloarm, z_axis, -22.85}, {lhand, y_axis, 14.77}, {rloarm, x_axis, -129.38}},
	{180, {luparm, z_axis, 0, 'move'}, {luparm, x_axis, -41.13}, {lelbow, z_axis, -11.25}, {lhand, y_axis, -9.84},
		{rloarm, x_axis, -136.76}},
	{100, {luparm, x_axis, -39.73}, {lelbow, z_axis, -10.19}, {rloarm, x_axis, -102.30}},
	{90, {ruparm, x_axis, -122.70}, {luparm, x_axis, -39.02}, {lelbow, z_axis, -9.84}, {rloarm, x_axis, -60.82}},
	{80, {ruparm, x_axis, -90.00}, {luparm, x_axis, -38.67}, {lelbow, z_axis, -7.03}},
	{80, {ruparm, x_axis, -42.89}, {luparm, x_axis, -37.27}, {lelbow, z_axis, -5.27}},
	{80, {ruparm, x_axis, -23.91}, {luparm, x_axis, -37.97}, {lelbow, z_axis, -2.81}},
	{30, {luparm, z_axis, 0, 'move'}, {rloarm, y_axis, 0, 'move'}, {ruparm, x_axis, -17.93}, {luparm, x_axis, -36.56},
		{lelbow, z_axis, 0}, {lloarm, z_axis, -22.15}, {lhand, y_axis, -43.94}, {rloarm, x_axis, -67.85}},
}

local function SetFrame(f)
	for i = 2, #f do
		local k = f[i]
		if k[4] == 'move' then Move(k[1], k[2], k[3]) else Turn(k[1], k[2], rad(k[3])) end
	end
end

local function Play(frames)
	for _, f in ipairs(frames) do
		SetFrame(f)
		Sleep(f[1])
	end
end

function script.Create()
	Hide(gun)
	Show(backgun)
	SetFrame(HOLSTER[#HOLSTER])       -- the arms carry the COB's holstered pose
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(torso, y_axis, 0, rad(90))
	SetSignalMask(0)
	busy = true
	StartThread(Play, HOLSTER)
	Sleep(530)
	Show(backgun)
	Hide(gun)
	Sleep(640)
	holstered = true
	busy = false
	WaitForTurn(torso, y_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	local waited = false
	while busy do
		waited = true
		Sleep(100)
	end
	if waited then
		SetSignalMask(0)
		Signal(SIG_AIM)
		SetSignalMask(SIG_AIM)
	end
	Turn(torso, y_axis, heading, rad(90))
	if holstered then
		SetSignalMask(0)
		busy = true
		StartThread(Play, DRAW)
		Sleep(400)
		Show(gun)
		Hide(backgun)
		Sleep(380)
		holstered = false
		busy = false
		SetSignalMask(SIG_AIM)
	end
	Turn(gun, x_axis, -pitch, rad(90))
	WaitForTurn(torso, y_axis)
	WaitForTurn(gun, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return flash                  -- COB: piece 2
end

function script.FireWeapon(num)
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local DEATH = {backgun, flash, ground, gun, lelbow, lhand, lleg, lloarm, lthigh, luparm, pelvis, rleg, rloarm, rthigh, ruparm}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(torso, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(torso, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(torso, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 3
end
