-- Advanced Construction Kbot (CORE_T2_BOT_AdvancedConstructor): Lua unit script for the remodelled walker (standard
-- QUAD skeleton: TA's four spike legs). Ported from TA's CORE_T2_BOT_AdvancedConstructor.COB: Activate/StartBuilding
-- queue RequestState(0) -> Go (open: the two nano cases slide out sideways, swing 90 deg, the end doors flap open and
-- the guns telescope 11.9 elmo; then the torso turns to the build heading at 160 deg/s and INBUILDSTANCE is set);
-- Deactivate/StopBuilding -> Stop (heading back, close). QueryNanoPiece alternates rnanospray/lnanospray, SweetSpot
-- = torso; speeds, sleeps and the death table are the COB's (old fore/hind legs -> the quad's thighs). COB move-x and
-- turn-z values are sign-flipped (Recoil CobInstance.h "COBWTF"). The walk is the shared quad walk.

pelvis, legs = piece('pelvis', 'legs')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')
ground, torso = piece('ground', 'torso')
lnanocase, lgunjoint, lnanogun, lnanospray, lcasedoor = piece('lnanocase', 'lgunjoint', 'lnanogun', 'lnanospray', 'lcasedoor')
rnanocase, rgunjoint, rnanogun, rnanospray, rcasedoor = piece('rnanocase', 'rgunjoint', 'rnanogun', 'rnanospray', 'rcasedoor')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Quad()

local rad = math.rad
local buildHeading = 0
local nano = 0

local function open()
	Move(lnanocase, x_axis, 0)
	Move(lnanocase, x_axis, 7.25, 14.133)
	Move(rnanocase, x_axis, 0)
	Move(rnanocase, x_axis, -7, 13.645)
	Move(rcasedoor, x_axis, 0)
	Move(lcasedoor, x_axis, 0)
	Sleep(513)
	Turn(lnanocase, y_axis, rad(-90), rad(173.74))
	Turn(rnanocase, y_axis, rad(90), rad(173.74))
	Turn(rcasedoor, z_axis, rad(90), rad(173.74))
	Turn(lcasedoor, z_axis, rad(-90), rad(173.74))
	Sleep(518)
	Move(rgunjoint, x_axis, -9, 22.837)
	Move(lgunjoint, x_axis, 9, 22.837)
	Sleep(520)
	Sleep(21)
end

local function close()
	Move(lnanocase, x_axis, 7.25)
	Move(rnanocase, x_axis, -7)
	Move(rgunjoint, x_axis, -9)
	Move(rgunjoint, x_axis, 0, 17.387)
	Move(rcasedoor, x_axis, 0)
	Move(lgunjoint, x_axis, 9)
	Move(lgunjoint, x_axis, 0, 17.387)
	Move(lcasedoor, x_axis, 0)
	Turn(lnanocase, y_axis, rad(-90))
	Turn(rnanocase, y_axis, rad(90))
	Turn(rcasedoor, z_axis, rad(90))
	Turn(lcasedoor, z_axis, rad(-90))
	Sleep(683)
	Turn(lnanocase, y_axis, rad(0), rad(130.62))
	Turn(rnanocase, y_axis, rad(0), rad(130.62))
	Turn(rcasedoor, z_axis, rad(-0.35), rad(131.13))
	Turn(lcasedoor, z_axis, rad(0), rad(130.62))
	Sleep(689)
	Move(lnanocase, x_axis, 0, 10.492)
	Move(rnanocase, x_axis, 0, 10.13)
	Sleep(691)
	Sleep(34)
end
local function Go()
	open()
	Turn(torso, y_axis, buildHeading, rad(160))
	WaitForTurn(torso, y_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

local function Stop()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	Turn(torso, y_axis, 0, rad(160))
	WaitForTurn(torso, y_axis)
	close()
end

-- COB RequestState: one worker runs Go/Stop until the requested state stops changing (0 = open, 1 = closed)
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
	StartThread(SmokeUnit, {torso})
end

function script.Activate()
	StartThread(RequestState, 0)
end

function script.Deactivate()
	StartThread(RequestState, 1)
end

function script.StartBuilding(heading, pitch)
	buildHeading = heading
	StartThread(RequestState, 0)
end

function script.StopBuilding()
	StartThread(RequestState, 1)
end

function script.QueryNanoPiece()
	local p = (nano == 0) and rnanospray or lnanospray   -- COB: pieces 0 / 1
	nano = 1 - nano
	return p
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 2
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({ground, lcasedoor, lfthigh, lgunjoint, lbthigh, lnanocase, lnanogun, lnanospray, pelvis, rcasedoor, rfthigh, rgunjoint, rbthigh, rnanocase, rnanogun, rnanospray, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({ground, lcasedoor, lfthigh, lgunjoint, lbthigh, lnanogun, lnanospray, pelvis, rcasedoor, rfthigh, rgunjoint, rbthigh, rnanogun, rnanospray}, SFX.FALL)
		Blow({lnanocase, rnanocase}, SFX.NONE)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({ground, lcasedoor, lfthigh, lgunjoint, lbthigh, lnanogun, lnanospray, pelvis, rcasedoor, rfthigh, rgunjoint, rbthigh, rnanogun, rnanospray}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({lnanocase, rnanocase}, SFX.NONE)
		Blow({torso}, SFX.SHATTER)
		return 2
	end
	Blow({ground, lcasedoor, lfthigh, lgunjoint, lbthigh, lnanogun, lnanospray, pelvis, rcasedoor, rfthigh, rgunjoint, rbthigh, rnanogun, rnanospray}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({lnanocase, rnanocase}, SFX.NONE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 2
end
