-- Maverick (ARM_T2_BOT_Maverick): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Maverick.COB. The pistols live in hip holsters (TA hid them in the legs; the old leg
-- shells rlegmain/llegmain are static holsters on the pelvis now, with their doors and holstered pistols): the first
-- aim runs the COB's RequestState(0) -> Go = ready (doors open, holstered pistols swing out, arms reach down), swap
-- the holstered pistols for the hand guns, ready2 (arms come up level, doors close); the torso then turns to the
-- heading at 150 deg/s. After the restore delay (reload * 2) the torso turns back at 200 deg/s and RequestState(1) ->
-- Stop = holster + holster2 puts them away. Shots alternate flare1/flare2 with the COB's barrel kick (2.5 elmo, back
-- at 37.5 elmo/s). All keyframes, speeds and sleeps are the COB's; turn-z values are sign-flipped (Recoil
-- CobInstance.h "COBWTF"), the hip bob of the old `hips` piece is dropped (the shared walk owns the pelvis), and
-- zero-speed COB turns/moves (no-ops) are left out. Death table and corpse types are the COB's.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, torso, head = piece('groundx2', 'torso', 'head')
rshoulder, ruparm, rarm, rgunbase, rgunshaft, rgunbarrel, flare1 =
	piece('rshoulder', 'ruparm', 'rarm', 'rgunbase', 'rgunshaft', 'rgunbarrel', 'flare1')
lshoulder, luparm, larm, lgunbase, lgunshaft, lgunbarrel, flare2 =
	piece('lshoulder', 'luparm', 'larm', 'lgunbase', 'lgunshaft', 'lgunbarrel', 'flare2')
rlegmain, rlegdoor, rgunhide, llegmain, llegdoor, lgunhide =
	piece('rlegmain', 'rlegdoor', 'rgunhide', 'llegmain', 'llegdoor', 'lgunhide')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 2000
local drawn = false           -- COB static 0: hand guns drawn
local gun = 0                 -- COB static 1: 0 = right fires next

local function ready()
	Move(torso, y_axis, 0)
	Move(head, z_axis, 0)
	Move(luparm, x_axis, 0)
	Move(lgunbase, y_axis, 0)
	Move(lgunshaft, x_axis, 0)
	Move(ruparm, x_axis, 0)
	Move(rgunbase, y_axis, 0)
	Move(rgunshaft, x_axis, 0)
	Turn(luparm, z_axis, rad(0))
	Turn(luparm, z_axis, rad(23.2), rad(140.62))
	Turn(larm, x_axis, rad(0))
	Turn(larm, x_axis, rad(-28.83), rad(174.72))
	Turn(ruparm, z_axis, rad(0))
	Turn(ruparm, z_axis, rad(-22.85), rad(138.49))
	Turn(rarm, x_axis, rad(0))
	Turn(rarm, x_axis, rad(-28.48), rad(172.58))
	Sleep(165)
	Turn(llegdoor, y_axis, rad(90), rad(517.24))
	Turn(rlegdoor, y_axis, rad(-90), rad(517.24))
	Turn(rshoulder, x_axis, rad(19.34), rad(111.12))
	Turn(lshoulder, x_axis, rad(19.34), rad(111.12))
	Turn(luparm, z_axis, rad(28.12), rad(28.28))
	Turn(larm, x_axis, rad(-40.43), rad(66.67))
	Turn(ruparm, z_axis, rad(-28.12), rad(30.31))
	Turn(rarm, x_axis, rad(-41.13), rad(72.73))
	Sleep(174)
	Move(lgunhide, y_axis, 1.25, 6.793)
	Move(rgunhide, y_axis, 1.25, 6.793)
	Turn(llegdoor, y_axis, rad(144.14), rad(294.24))
	Turn(lgunhide, z_axis, rad(45), rad(244.56))
	Turn(rlegdoor, y_axis, rad(-144.84), rad(298.06))
	Turn(rgunhide, z_axis, rad(-45), rad(244.56))
	Turn(rshoulder, x_axis, rad(54.84), rad(192.97))
	Turn(lshoulder, x_axis, rad(54.14), rad(189.15))
	Turn(luparm, z_axis, rad(34.8), rad(36.3))
	Turn(larm, x_axis, rad(-64.69), rad(131.84))
	Turn(ruparm, z_axis, rad(-34.8), rad(36.3))
	Turn(rarm, x_axis, rad(-64.34), rad(126.1))
	Sleep(184)
	Move(lgunhide, y_axis, 2.5, 5.252)
	Move(rgunhide, y_axis, 2.5, 5.252)
	Turn(lgunhide, z_axis, rad(90), rad(189.07))
	Turn(rgunhide, z_axis, rad(-90), rad(189.07))
	Sleep(238)
	Turn(rshoulder, x_axis, rad(66.09), rad(98.68))
	Turn(lshoulder, x_axis, rad(66.8), rad(111.02))
	Turn(luparm, z_axis, rad(15.12), rad(172.69))
	Turn(larm, x_axis, rad(-90), rad(222.04))
	Turn(ruparm, z_axis, rad(-15.11), rad(172.69))
	Turn(rarm, x_axis, rad(-90), rad(225.12))
	Sleep(114)
	Sleep(70)
end

local function ready2()
	Move(torso, y_axis, 0)
	Move(lgunhide, y_axis, 2.5)
	Move(lgunhide, y_axis, 0, 35.714)
	Move(rgunhide, y_axis, 2.5)
	Move(rgunhide, y_axis, 0, 35.714)
	Move(head, z_axis, 0)
	Move(luparm, x_axis, 0)
	Move(lgunbase, y_axis, 0)
	Move(lgunshaft, x_axis, 0)
	Move(lgunshaft, y_axis, 0)
	Move(lgunshaft, y_axis, 5.125, 73.214)
	Move(lgunbarrel, y_axis, 0)
	Move(lgunbarrel, y_axis, 2.75, 39.286)
	Move(ruparm, x_axis, 0)
	Move(rgunbase, y_axis, 0)
	Move(rgunshaft, x_axis, 0)
	Move(rgunshaft, y_axis, 0)
	Move(rgunshaft, y_axis, 5.25, 75)
	Move(rgunbarrel, y_axis, 0)
	Move(rgunbarrel, y_axis, 2.625, 37.5)
	Turn(llegdoor, y_axis, rad(144.14))
	Turn(lgunhide, z_axis, rad(90))
	Turn(lgunhide, z_axis, rad(0), rad(1285.71))
	Turn(rlegdoor, y_axis, rad(-144.84))
	Turn(rgunhide, z_axis, rad(-90))
	Turn(rgunhide, z_axis, rad(0), rad(1285.71))
	Turn(rshoulder, x_axis, rad(35.16))
	Turn(rshoulder, x_axis, rad(13.71), rad(306.36))
	Turn(lshoulder, x_axis, rad(35.16))
	Turn(lshoulder, x_axis, rad(13.36), rad(311.38))
	Turn(luparm, z_axis, rad(0))
	Turn(luparm, z_axis, rad(24.61), rad(351.56))
	Turn(larm, x_axis, rad(-52.38))
	Turn(larm, x_axis, rad(-32.34), rad(286.27))
	Turn(ruparm, z_axis, rad(0))
	Turn(ruparm, z_axis, rad(-24.61), rad(351.56))
	Turn(rarm, x_axis, rad(-52.03))
	Turn(rarm, x_axis, rad(-32.34), rad(281.25))
	Sleep(70)
	Move(lgunshaft, y_axis, 4.625, 6.25)
	Move(rgunshaft, y_axis, 4.375, 10.938)
	Turn(llegdoor, y_axis, rad(120.94), rad(290.04))
	Turn(rlegdoor, y_axis, rad(-120.23), rad(307.61))
	Turn(rshoulder, x_axis, rad(0), rad(171.39))
	Turn(lshoulder, x_axis, rad(0), rad(166.99))
	Turn(luparm, z_axis, rad(20.04), rad(57.12))
	Turn(larm, x_axis, rad(-30.94), rad(17.58))
	Turn(ruparm, z_axis, rad(-20.03), rad(57.12))
	Turn(rarm, x_axis, rad(-30.94), rad(17.58))
	Sleep(80)
	Move(lgunshaft, y_axis, 2.75, 31.25)
	Move(lgunbarrel, y_axis, 3.875, 18.75)
	Move(rgunshaft, y_axis, 2.5, 31.25)
	Move(rgunbarrel, y_axis, 4.5, 31.25)
	Turn(llegdoor, y_axis, rad(100.55), rad(339.84))
	Turn(rlegdoor, y_axis, rad(-100.2), rad(333.98))
	Turn(rshoulder, x_axis, rad(-41.48), rad(691.4))
	Turn(lshoulder, x_axis, rad(-41.13), rad(685.55))
	Turn(luparm, z_axis, rad(11.25), rad(146.48))
	Turn(larm, x_axis, rad(-17.23), rad(228.52))
	Turn(ruparm, z_axis, rad(-11.25), rad(146.48))
	Turn(rarm, x_axis, rad(-16.52), rad(240.23))
	Sleep(60)
	Move(lgunshaft, y_axis, 4.25, 30)
	Move(lgunbarrel, y_axis, 2.5, 27.5)
	Move(rgunshaft, y_axis, 4.125, 32.5)
	Move(rgunbarrel, y_axis, 2.625, 37.5)
	Turn(llegdoor, y_axis, rad(80.86), rad(393.75))
	Turn(rlegdoor, y_axis, rad(-80.16), rad(400.78))
	Turn(rshoulder, x_axis, rad(-68.2), rad(534.38))
	Turn(lshoulder, x_axis, rad(-68.2), rad(541.41))
	Turn(luparm, z_axis, rad(0), rad(225))
	Turn(larm, x_axis, rad(0), rad(344.53))
	Turn(ruparm, z_axis, rad(0), rad(225))
	Turn(rarm, x_axis, rad(0), rad(330.47))
	Sleep(50)
	Move(lgunshaft, y_axis, 3.25, 20)
	Move(lgunbarrel, y_axis, 2.875, 7.5)
	Move(rgunshaft, y_axis, 3.75, 7.5)
	Turn(llegdoor, y_axis, rad(60.82), rad(400.78))
	Turn(rlegdoor, y_axis, rad(-60.11), rad(400.78))
	Turn(rshoulder, x_axis, rad(-90), rad(435.94))
	Turn(lshoulder, x_axis, rad(-90), rad(435.94))
	Sleep(50)
	Move(lgunshaft, y_axis, 1.75, 21.429)
	Move(lgunbarrel, y_axis, 2.25, 8.929)
	Move(rgunshaft, y_axis, 1.5, 32.143)
	Move(rgunbarrel, y_axis, 2.75, 1.786)
	Turn(llegdoor, y_axis, rad(30.94), rad(426.9))
	Turn(rlegdoor, y_axis, rad(-30.59), rad(421.88))
	Sleep(70)
	Move(lgunshaft, y_axis, 0, 25)
	Move(lgunbarrel, y_axis, 2.75, 7.143)
	Move(rgunshaft, y_axis, 0, 21.429)
	Move(rgunbarrel, y_axis, 2.875, 1.786)
	Turn(llegdoor, y_axis, rad(0), rad(441.96))
	Turn(rlegdoor, y_axis, rad(0), rad(436.94))
	Sleep(70)
	Move(lgunbarrel, y_axis, 0, 55)
	Move(rgunbarrel, y_axis, 0, 57.5)
	Sleep(50)
	Sleep(10)
end

local function holster()
	Move(torso, y_axis, 0)
	Move(head, z_axis, 0)
	Move(luparm, x_axis, 0)
	Move(lgunshaft, x_axis, 0)
	Move(lgunshaft, y_axis, 0)
	Move(lgunshaft, y_axis, 2.625, 17.857)
	Move(ruparm, x_axis, 0)
	Move(rgunshaft, x_axis, 0)
	Move(rgunshaft, y_axis, 0)
	Move(rgunshaft, y_axis, 2.5, 17.007)
	Turn(rshoulder, x_axis, rad(-90))
	Turn(lshoulder, x_axis, rad(-90))
	Turn(lgunbase, y_axis, rad(0))
	Turn(lgunbase, y_axis, rad(45), rad(306.12))
	Turn(rgunbase, y_axis, rad(0))
	Turn(rgunbase, y_axis, rad(-45), rad(306.12))
	Sleep(147)
	Move(lgunbarrel, y_axis, 5.625, 37.5)
	Move(rgunbarrel, y_axis, 5.5, 36.667)
	Turn(llegdoor, y_axis, rad(90), rad(600))
	Turn(rlegdoor, y_axis, rad(-90), rad(600))
	Turn(lgunbase, y_axis, rad(90), rad(300))
	Turn(rgunbase, y_axis, rad(-90), rad(300))
	Sleep(150)
	Turn(llegdoor, y_axis, rad(144.84), rad(287.14))
	Turn(rlegdoor, y_axis, rad(-144.49), rad(285.3))
	Turn(rshoulder, x_axis, rad(-39.38), rad(265.05))
	Turn(lshoulder, x_axis, rad(-36.21), rad(281.62))
	Turn(luparm, z_axis, rad(35.5), rad(185.9))
	Turn(lgunbase, y_axis, rad(-90), rad(942.41))
	Turn(ruparm, z_axis, rad(-35.16), rad(184.06))
	Sleep(191)
	Turn(rshoulder, x_axis, rad(0), rad(281.25))
	Turn(lshoulder, x_axis, rad(0), rad(258.65))
	Turn(luparm, z_axis, rad(40.08), rad(32.64))
	Turn(lgunbase, y_axis, rad(45), rad(964.28))
	Turn(ruparm, z_axis, rad(-38.31), rad(22.6))
	Turn(rgunbase, y_axis, rad(-45), rad(321.43))
	Sleep(140)
	Turn(lgunbase, y_axis, rad(0), rad(409.09))
	Turn(rgunbase, y_axis, rad(0), rad(409.09))
	Sleep(110)
	Turn(luparm, z_axis, rad(26.72), rad(139.16))
	Turn(ruparm, z_axis, rad(-28.12), rad(106.2))
	Sleep(96)
	Move(rshoulder, y_axis, 2.625, 11.315)
	Move(lshoulder, y_axis, 2.875, 12.392)
	Turn(luparm, z_axis, rad(38.67), rad(51.52))
	Turn(larm, z_axis, rad(-43.94), rad(189.42))
	Turn(ruparm, z_axis, rad(-37.27), rad(39.4))
	Turn(rarm, z_axis, rad(43.24), rad(186.39))
	Sleep(232)
	Move(rshoulder, y_axis, 0, 19.59)
	Move(lshoulder, y_axis, 0, 21.455)
	Turn(luparm, z_axis, rad(14.77), rad(178.4))
	Turn(larm, z_axis, rad(-33.75), rad(76.08))
	Turn(ruparm, z_axis, rad(-17.92), rad(144.29))
	Turn(rarm, z_axis, rad(36.56), rad(49.84))
	Sleep(134)
	Turn(luparm, z_axis, rad(0), rad(175.78))
	Turn(larm, z_axis, rad(0), rad(401.78))
	Turn(ruparm, z_axis, rad(0), rad(213.45))
	Turn(rarm, z_axis, rad(0), rad(435.27))
	Sleep(84)
	Sleep(84)
end

local function holster2()
	Move(torso, y_axis, 0)
	Move(head, z_axis, 0)
	Move(rshoulder, y_axis, -1.75)
	Move(rshoulder, y_axis, -1.25, 2.941)
	Move(lshoulder, y_axis, -1.75)
	Move(lshoulder, y_axis, -1.25, 2.941)
	Move(luparm, x_axis, 0)
	Move(lgunbase, y_axis, 0)
	Move(lgunshaft, x_axis, 0)
	Move(lgunshaft, y_axis, 2.625)
	Move(lgunbarrel, y_axis, 5.625)
	Move(ruparm, x_axis, 0)
	Move(rgunbase, y_axis, 0)
	Move(rgunshaft, x_axis, 0)
	Move(rgunshaft, y_axis, 2.5)
	Move(rgunbarrel, y_axis, 5.5)
	Turn(llegdoor, y_axis, rad(144.84))
	Turn(lgunhide, z_axis, rad(90))
	Turn(rlegdoor, y_axis, rad(-144.49))
	Turn(rgunhide, z_axis, rad(-90))
	Turn(luparm, z_axis, rad(-4.57))
	Turn(luparm, z_axis, rad(-2.81), rad(10.34))
	Turn(ruparm, z_axis, rad(3.87))
	Turn(ruparm, z_axis, rad(2.81), rad(6.2))
	Sleep(170)
	Turn(lgunhide, z_axis, rad(45), rad(375))
	Turn(rgunhide, z_axis, rad(-45), rad(375))
	Turn(rshoulder, x_axis, rad(-36.91), rad(307.62))
	Turn(lshoulder, x_axis, rad(-35.16), rad(292.97))
	Turn(luparm, z_axis, rad(22.5), rad(210.94))
	Turn(ruparm, z_axis, rad(-22.15), rad(208))
	Sleep(120)
	Turn(llegdoor, y_axis, rad(90), rad(365.62))
	Turn(lgunhide, z_axis, rad(0), rad(300))
	Turn(rlegdoor, y_axis, rad(-90), rad(363.28))
	Turn(rgunhide, z_axis, rad(0), rad(300))
	Turn(rshoulder, x_axis, rad(-39.38), rad(16.4))
	Turn(lshoulder, x_axis, rad(-39.38), rad(28.12))
	Turn(luparm, z_axis, rad(29.18), rad(44.53))
	Turn(ruparm, z_axis, rad(-31.99), rad(65.62))
	Sleep(150)
	Turn(llegdoor, y_axis, rad(0), rad(600))
	Turn(rlegdoor, y_axis, rad(0), rad(600))
	Turn(rshoulder, x_axis, rad(-43.59), rad(28.12))
	Turn(lshoulder, x_axis, rad(-45.7), rad(42.19))
	Turn(luparm, z_axis, rad(38.67), rad(63.28))
	Turn(ruparm, z_axis, rad(-44.65), rad(84.38))
	Sleep(150)
	Turn(rshoulder, x_axis, rad(-28.12), rad(103.12))
	Turn(lshoulder, x_axis, rad(-30.94), rad(98.44))
	Turn(luparm, z_axis, rad(17.58), rad(140.62))
	Turn(ruparm, z_axis, rad(-14.06), rad(203.91))
	Sleep(150)
	Turn(rshoulder, x_axis, rad(0), rad(187.5))
	Turn(lshoulder, x_axis, rad(0), rad(206.25))
	Turn(luparm, z_axis, rad(0), rad(117.19))
	Turn(ruparm, z_axis, rad(0), rad(93.75))
	Sleep(150)
	Sleep(10)
end
local function Go()
	ready()
	Hide(rgunhide); Hide(lgunhide)
	Show(lgunbarrel); Show(lgunshaft); Show(lgunbase)
	Show(rgunbarrel); Show(rgunshaft); Show(rgunbase)
	ready2()
	drawn = true
end

local function Stop()
	drawn = false
	holster()
	Show(rgunhide); Show(lgunhide)
	Hide(lgunbarrel); Hide(lgunshaft); Hide(lgunbase)
	Hide(rgunbarrel); Hide(rgunshaft); Hide(rgunbase)
	holster2()
end

-- COB RequestState: one worker runs Go/Stop until the requested state stops changing (0 = drawn, 1 = holstered)
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then Go() else Stop() end
	end
	busy = false
end

function script.Create()
	Hide(lgunbarrel); Hide(lgunshaft); Hide(lgunbase)
	Hide(rgunbarrel); Hide(rgunshaft); Hide(rgunbase)
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	SetSignalMask(0)
	StartThread(RequestState, 1)
	Turn(torso, y_axis, 0, rad(200))
end

function script.AimWeapon(num, heading, pitch)
	StartThread(RequestState, 0)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	while not drawn do
		Sleep(250)
	end
	Turn(torso, y_axis, heading, rad(150))
	WaitForTurn(torso, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

local function Kick(barrel)
	Move(barrel, y_axis, 2.5)
	Sleep(150)
	Move(barrel, y_axis, 0, 37.5)
end

function script.FireWeapon(num)
	StartThread(Kick, (gun == 0) and rgunbarrel or lgunbarrel)
	gun = 1 - gun
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 2
end

function script.QueryWeapon(num)
	return (gun == 0) and flare1 or flare2
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 2
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
		return 1
	elseif severity <= 50 then
		Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
		return 2
	elseif severity <= 99 then
		Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
		return 3
	end
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
