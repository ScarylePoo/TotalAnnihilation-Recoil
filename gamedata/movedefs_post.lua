-- After the movement classes are built (gamedata/movedefs.lua): a unit tag that contradicts its class (water depth,
-- slope...) is set to the class's value, so the unit def says what the unit really does. (Splinter Faction's.)

local tagList = VFS.Include("gamedata/movedefs_tags.lua")

local byName = {}
for _, md in pairs(MoveDefs) do
	byName[string.lower(md.name)] = md
end

for _, ud in pairs(DEFS.unitDefs) do
	local md = ud.movementclass and byName[string.lower(ud.movementclass)]
	if md then
		for tagName in pairs(tagList) do
			tagName = string.lower(tagName)
			if md[tagName] ~= nil and ud[tagName] ~= nil and ud[tagName] ~= md[tagName] then
				ud[tagName] = md[tagName]
			end
		end
	end
end
