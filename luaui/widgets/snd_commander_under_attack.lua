function widget:GetInfo()
	return {
		name    = "Commander Under Attack",
		desc    = "Plays TA's commander alarm when your commander takes damage",
		author  = "Scary le Poo",
		date    = "2026-11-22",
		license = "GNU GPL, v2 or later",
		layer   = 0,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- Total Annihilation sounded a klaxon (warning2.wav) whenever your commander was hit. The unit defs still name it
-- (sounds.underattack = "warning2"), but the engine no longer plays that entry, so this widget does.
--  * your own commander only (customparams.iscommander); decoys stay silent, as they are not worth the alarm
--  * real damage only: no paralysis, no self-inflicted or allied damage reports of zero
--  * at most once every COOLDOWN seconds, so a sustained attack repeats the alarm without stacking it
-- The sound is a GUI sound in gamedata/sounds.lua (not positional, never cut off).
--------------------------------------------------------------------------------

local ALARM    = "sounds/warning2.wav"
local VOLUME   = 1.0
local COOLDOWN = 6      -- seconds between alarms (the sound itself is 2.6 s long)

local isCommander = {}
for unitDefID, ud in pairs(UnitDefs) do
	local cp = ud.customParams
	if cp and cp.iscommander and not cp.isdecoycommander then
		isCommander[unitDefID] = true
	end
end

local myTeamID = Spring.GetMyTeamID()
local lastAlarm = -COOLDOWN

local function Refresh()
	myTeamID = Spring.GetMyTeamID()
	if Spring.GetSpectatingState() then
		widgetHandler:RemoveWidget()
	end
end

function widget:Initialize()
	Refresh()
end

function widget:PlayerChanged()
	Refresh()
end

function widget:UnitDamaged(unitID, unitDefID, unitTeam, damage, paralyzer)
	if unitTeam ~= myTeamID or not isCommander[unitDefID] then return end
	if paralyzer or not damage or damage <= 0 then return end
	local now = Spring.GetGameSeconds()
	if now - lastAlarm < COOLDOWN then return end
	lastAlarm = now
	Spring.PlaySoundFile(ALARM, VOLUME, "ui")
end
