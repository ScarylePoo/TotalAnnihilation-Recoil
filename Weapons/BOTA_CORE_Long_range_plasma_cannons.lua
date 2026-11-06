-- Weapon definitions (converted from BOTA_CORE_Long_range_plasma_cannons.TDF)

return {
	intimidator = {
		-- used by units
		-- CORE_T2_DEF_Intimidator
		-- type
		weapontype = "Cannon",
		turret = 1,
		ballistic = 1,
		-- visuals
		size = 40,
		rgbcolor = "1.0 0.5 0",
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
		weaponvelocity = 1000,  -- TA 3.1c (was 800)
		accuracy = 1000,  -- TA 3.1c (was 600)
		-- costs
		energypershot = 2000,  -- TA 3.1c (was 12000)
		-- stats
		range = 5120,
		reloadtime = 8,  -- TA 3.1c (was 23)
		areaofeffect = 100,
		damage = {
			default = 2400,  -- TA 3.1c (was 1800)
		},
	},
	buzzsaw = {
		-- used by units
		-- CORE_T2_DEF_Buzzsaw
		-- type
		weapontype = "Cannon",
		turret = 1,
		ballistic = 1,
		-- visuals
		size = 20,
		rgbcolor = "1.0 0.5 0",
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
		weaponvelocity = 900,  -- TA 3.1c (was 800)
		accuracy = 800,  -- TA 3.1c (was 700)
		-- costs
		energypershot = 2000,  -- TA 3.1c (was 4000)
		-- stats
		range = 3800,  -- TA 3.1c (was 4096)
		reloadtime = 0.5,  -- TA 3.1c (was 1.2)
		areaofeffect = 120,
		damage = {
			default = 1800,  -- TA 3.1c (was 450)
		},
	},
}
