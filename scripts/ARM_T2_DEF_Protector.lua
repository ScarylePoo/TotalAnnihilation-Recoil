-- Protector (ARM_T2_DEF_Protector): anti-nuke silo. Lua port of the BOTA COB (no BOS source in the repo).
-- Why a port: the COB's QueryPrimary/AimFromPrimary pick rocket1..3 from a counter that Create sets to 1, but the
-- engine queries the weapon pieces in InitWeapons BEFORE the COB Create runs; with the counter still 0 neither
-- function sets a piece, the engine gets -1 and logs "Neither AimFromWeapon nor QueryWeapon defined or returned
-- invalid pieceids". Here the counter starts at 1, so the query is valid from the first call.
-- Behaviour kept from the COB: the four doors fold open (aim) and close 2x reload time after the last aim; each
-- shot hides the fired missile, shows the next and turns the launcher 120 deg; same death explosions.
-- COB -> Lua: z-axis turn values are negated (the engine negates COB z turns); x/y unchanged.

include "smokeunit.lua"

local base, turret, rocket1, rocket2, rocket3, door1, door2, door3, door4 =
	piece('base', 'turret', 'rocket1', 'rocket2', 'rocket3', 'door1', 'door2', 'door3', 'door4')
local rockets = {rocket1, rocket2, rocket3}

local COBANG = 2 * math.pi / 65536          -- COB angle units -> radians
local SIG_AIM = 2

local gun = 1                               -- next missile to fire (COB static 2)
local restoreDelay = 3000                   -- ms (COB static 1; SetMaxReloadTime made it 2x the reload)
local state = 1                             -- 0 open, 1 closed (COB statechg_DesiredState)
local changing = false

local function Open()
	Turn(door1, z_axis, 0); Turn(door1, z_axis, 23592 * COBANG, 13344 * COBANG)
	Turn(door2, z_axis, 0); Turn(door2, z_axis, -23920 * COBANG, 13529 * COBANG)
	Turn(door3, x_axis, 0); Turn(door3, x_axis, -23429 * COBANG, 13251 * COBANG)
	Turn(door4, x_axis, 0); Turn(door4, x_axis, 23592 * COBANG, 13344 * COBANG)
	Sleep(1768)
	Sleep(3)
end

local function Close()
	Turn(door1, z_axis, 23592 * COBANG); Turn(door1, z_axis, 0, 13389 * COBANG)
	Turn(door2, z_axis, -23920 * COBANG); Turn(door2, z_axis, 0, 13575 * COBANG)
	Turn(door3, x_axis, -23429 * COBANG); Turn(door3, x_axis, 0, 13296 * COBANG)
	Turn(door4, x_axis, 23592 * COBANG); Turn(door4, x_axis, 0, 13389 * COBANG)
	Sleep(1762)
	Sleep(14)
end

local function RequestState(req)
	if changing then
		state = req
		return
	end
	changing = true
	local actual = state
	state = req
	while state ~= actual do
		if state == 0 then
			Open(); actual = 0
		elseif state == 1 then
			Close(); actual = 1
		end
	end
	changing = false
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	SetSignalMask(0)
	StartThread(RequestState, 1)
end

function script.Create()
	local w = UnitDefs[unitDefID].weapons[1]
	if w and WeaponDefs[w.weaponDef] then
		restoreDelay = WeaponDefs[w.weaponDef].reload * 1000 * 2
	end
	StartThread(SmokeUnit, {door1, door2, door3, door4})
end

function script.Activate()
	StartThread(RequestState, 0)
end

function script.Deactivate()
	StartThread(RequestState, 1)
end

function script.AimWeapon1(heading, pitch)
	StartThread(RequestState, 0)
	Sleep(1500)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	StartThread(RestoreAfterDelay)
	return true
end

function script.FireWeapon1()
	if gun == 1 then
		Hide(rocket1); Show(rocket2)
		Turn(turret, y_axis, 21845 * COBANG, 5461 * COBANG)
		WaitForTurn(turret, y_axis)
		Show(rocket3)
	elseif gun == 2 then
		Hide(rocket2); Show(rocket3)
		Turn(turret, y_axis, 43690 * COBANG, 5461 * COBANG)
		WaitForTurn(turret, y_axis)
	elseif gun == 3 then
		Hide(rocket3); Show(rocket1)
		Turn(turret, y_axis, 65536 * COBANG, 5461 * COBANG)
		WaitForTurn(turret, y_axis)
	end
	gun = gun + 1
	if gun == 4 then gun = 1 end
end

function script.QueryWeapon1()
	return rockets[gun]
end

function script.AimFromWeapon1()
	return rockets[gun]
end

function script.SweetSpot()
	return base
end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	local doors = {door1, door2, door3, door4}
	if severity <= 25 then
		Explode(base, SFX.NONE)
		for _, p in ipairs(doors) do Explode(p, SFX.NONE) end
		for _, p in ipairs(rockets) do Explode(p, SFX.NONE) end
		Explode(turret, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Explode(base, SFX.NONE)
		for _, p in ipairs(doors) do Explode(p, SFX.NONE) end
		for _, p in ipairs(rockets) do Explode(p, SFX.FALL) end
		Explode(turret, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	Explode(base, SFX.NONE)
	for _, p in ipairs(doors) do Explode(p, SFX.NONE) end
	for _, p in ipairs(rockets) do Explode(p, f) end
	Explode(turret, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 2
end
