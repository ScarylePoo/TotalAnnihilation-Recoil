function widget:GetInfo()
	return {
		name = "QueueCopypasta",
		desc = "Copy and paste orders: Space+Alt+number copies the selected units' queues, Space+number gives them to the selection",
		author = "dizekat",
		date = "2008",
		license = "GNU GPL, v2 or later",
		layer = 5,
		enabled = true
	}
end

--------------------------------------------------------------------------------
-- Space+Alt+0..9 copies the queues of the selected units into that slot; Space+0..9 appends a copied queue to each
-- selected unit (the copied queues are dealt out in turn when several units were copied). Slots last for the game.
--------------------------------------------------------------------------------

local queues = {}
local KEY_0 = Spring.GetKeyCode("0")

function widget:KeyPress(key, modifier, isRepeat)
	if not modifier.meta or isRepeat then
		return false
	end
	local slot = key - KEY_0
	if slot < 0 or slot > 9 then
		return false
	end
	local units = Spring.GetSelectedUnits()
	if modifier.alt then
		local copied = {}
		for _, unitID in ipairs(units) do
			local q = Spring.GetUnitCommands(unitID, -1)
			if q and #q > 0 then
				copied[#copied + 1] = q
			end
		end
		if #copied == 0 then
			return false
		end
		queues[slot] = copied
		return true
	end
	local copied = queues[slot]
	if not copied or #units == 0 then
		return false
	end
	for i, unitID in ipairs(units) do
		for _, cmd in ipairs(copied[1 + (i - 1) % #copied]) do
			Spring.GiveOrderToUnit(unitID, cmd.id, cmd.params, { "shift" })
		end
	end
	return true
end
