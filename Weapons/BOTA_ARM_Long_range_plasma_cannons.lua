-- Weapon definitions (native Recoil tags; converted from BOTA_ARM_Long_range_plasma_cannons.TDF)

return {
	big_bertha = {
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
		soundstart = "xplonuk4",
		soundhit = "xplonuk1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		tolerance = 300,
		weaponvelocity = 800,
		accuracy = 500,
		-- costs
		energypershot = 9000,
		-- stats
		range = 4608,
		reloadtime = 20,
		areaofeffect = 80,
		craterareaofeffect = 120,
		damage = {
			default = 1500,
		},
	},
	vulcan = {
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
		collidefriendly = 1,
		tolerance = 300,
		weaponvelocity = 800,
		accuracy = 700,
		-- costs
		energypershot = 4000,
		-- stats
		range = 3584,
		reloadtime = 1,
		areaofeffect = 100,
		craterareaofeffect = 150,
		damage = {
			default = 400,
		},
	},
}
