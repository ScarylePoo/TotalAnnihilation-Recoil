-- Weapon definitions (native Recoil tags; converted from BOTA_CORE_Long_range_plasma_cannons.TDF)

return {
	intimidator = {
		-- used by units
		-- type
		weapontype = "Cannon",
		turret = 1,
		-- visuals
		size = 40,
		rgbcolor = "1.0 0.5 0",
		gravityaffected = true,
		intensity = 0.2,
		explosiongenerator = "custom:LRPC_Expl",
		-- sounds
		soundstart = "xplonuk3",
		soundhit = "xplonuk1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		tolerance = 300,
		weaponvelocity = 800,
		accuracy = 600,
		-- costs
		energypershot = 12000,
		-- stats
		range = 5120,
		reloadtime = 23,
		areaofeffect = 100,
		craterareaofeffect = 150,
		damage = {
			default = 1800,
		},
	},
	buzzsaw = {
		-- used by units
		-- type
		weapontype = "Cannon",
		turret = 1,
		-- visuals
		size = 20,
		rgbcolor = "1.0 0.5 0",
		gravityaffected = true,
		intensity = 0.2,
		explosiongenerator = "custom:LRPC_Expl",
		-- sounds
		soundstart = "xplonuk4",
		soundhit = "xplonuk1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		tolerance = 300,
		weaponvelocity = 800,
		accuracy = 700,
		-- costs
		energypershot = 4000,
		-- stats
		range = 4096,
		reloadtime = 1.2,
		areaofeffect = 120,
		craterareaofeffect = 180,
		damage = {
			default = 450,
		},
	},
}
