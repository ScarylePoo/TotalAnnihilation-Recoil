-- Weapon definitions (converted from BOTA_SHARED_Building_selfdestructs.TDF)

return {
	small_building = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 205,
		soundstart = "largegun",
		soundhit = "xplosml3",
		damage = {
			default = 900,
		},
	},
	medium_building = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 325,
		soundstart = "largegun",
		soundhit = "xplomed1",
		damage = {
			default = 1400,
		},
	},
	large_building = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 400,
		soundstart = "largegun",
		soundhit = "xplolrg4",
		damage = {
			default = 1800,
		},
	},
	estor_building = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 420,
		soundstart = "largegun",
		soundhit = "xplonuk1",
		damage = {
			default = 1900,
		},
	},
	atomic_blast = {
		-- used by units
		-- type
		rendertype = 4,
		turret = 1,
		ballistic = 1,
		-- visuals
		-- sounds
		soundstart = "largegun",
		soundhit = "xplonuk3",
		-- behaviour
		weaponvelocity = 250,
		-- stats
		range = 480,
		reloadtime = 3.6,
		areaofeffect = 516,
		damage = {
			default = 2000,
		},
	},
}
