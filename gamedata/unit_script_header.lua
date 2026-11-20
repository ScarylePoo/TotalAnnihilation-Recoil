-- Author: Tobi Vollebregt (the engine's default header), with TA:Recoil's aim speed added below.

-- This is prepended before each actual unitscript, so certain functions and
-- variables can be localized, without copy pasting this into every file.

-- Do not overuse this:
-- there is a limit of 200 locals and 60 upvalues per Lua function!

local unitID = unitID
local unitDefID = unitDefID
local UnitDef = UnitDefs[unitDefID]

local UnitScript = Spring.UnitScript

local EmitSfx = UnitScript.EmitSfx
local Explode = UnitScript.Explode
local GetUnitValue = UnitScript.GetUnitValue
local SetUnitValue = UnitScript.SetUnitValue
local Hide = UnitScript.Hide
local Show = UnitScript.Show

local Move = UnitScript.Move
local Turn = UnitScript.Turn
-- TA:Recoil: every turn a script makes while aiming a weapon is AIM_TURN_SPEED times as fast as written
-- (the scripts keep TA's own aim speeds). "While aiming" is the thread the framework runs AimWeapon in:
-- the callin is wrapped as the script defines it and marks its thread, and Turn looks for the mark.
-- Turns made by other threads (walking, restoring after a delay) are as written.
-- (This file is joined into one line with comments cut at two dashes, so no two dashes inside a string.)
do
	local AIM_TURN_SPEED = 1.5
	local rawTurn = UnitScript.Turn
	local running = coroutine.running
	-- (one table per unit, shared by the script and the files it includes: each of them gets this header)
	local aiming = __aimThreads
	if not aiming then
		aiming = setmetatable({}, { __mode = "k" })
		__aimThreads = aiming
	end
	Turn = function(piece, axis, destination, speed)
		if speed and aiming[running()] then speed = speed * AIM_TURN_SPEED end
		return rawTurn(piece, axis, destination, speed)
	end
	local watch = {}
	watch.__newindex = function(t, key, value)
		if type(value) == "function" and type(key) == "string" and key:find("^AimWeapon") then
			local aim = value
			value = function(...)
				local co = running()
				if co then aiming[co] = true end
				return aim(...)
			end
		end
		-- (unit scripts have no rawset: lift the metatable for the write)
		setmetatable(t, nil)
		t[key] = value
		setmetatable(t, watch)
	end
	setmetatable(script, watch)
end

local Spin = UnitScript.Spin
local StopSpin = UnitScript.StopSpin
local Scale = UnitScript.Scale

local MultiSetPieceVisibility = UnitScript.MultiSetPieceVisibility
local MultiMove = UnitScript.MultiMove
local MultiTurn = UnitScript.MultiTurn
local MultiSpin = UnitScript.MultiSpin
local MultiStopSpin = UnitScript.MultiStopSpin
local MultiScale = UnitScript.MultiScale
local MultiExplode = UnitScript.MultiExplode

local StartThread = UnitScript.StartThread
local Signal = UnitScript.Signal
local SetSignalMask = UnitScript.SetSignalMask
local Sleep = UnitScript.Sleep
local WaitForMove = UnitScript.WaitForMove
local WaitForTurn = UnitScript.WaitForTurn
local WaitForScale = UnitScript.WaitForScale

local x_axis = 1
local y_axis = 2
local z_axis = 3
