-- Weapon definitions (converted from BOTA_ARM_Long_range_plasma_cannons.TDF)

return {
	big_bertha = {
		-- used by units
		-- ARM_T2_DEF_BigBertha
		-- type
		weapontype = "Cannon",
		turret = 1,
		ballistic = 1,
		-- visuals
		size = 40,
		rgbcolor = "1.0 0.5 0",
		intensity = 0.2,
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
		energypershot = 1500,  -- TA 3.1c (was 9000)
		-- stats
		range = 4096,  -- TA 3.1c (was 4608)
		reloadtime = 7,  -- TA 3.1c (was 20)
		areaofeffect = 80,
		damage = {
			default = 2000,  -- TA 3.1c (was 1500)
		},
	},
	vulcan = {
		-- used by units
		-- ARM_T2_DEF_Vulcan
		-- type
		weapontype = "Cannon",
		turret = 1,
		ballistic = 1,
		-- visuals
		size = 20,
		rgbcolor = "1.0 0.5 0",
		intensity = 0.2,
		-- sounds
		soundstart = "xplonuk4",
		soundhit = "xplonuk1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		tolerance = 300,
		weaponvelocity = 800,
		accuracy = 800,  -- TA 3.1c (was 700)
		-- costs
		energypershot = 2000,  -- TA 3.1c (was 4000)
		-- stats
		range = 3080,  -- TA 3.1c (was 3584)
		reloadtime = 0.25,  -- TA 3.1c (was 1)
		areaofeffect = 100,
		damage = {
			default = 1000,  -- TA 3.1c (was 400)
		},
	},
}
