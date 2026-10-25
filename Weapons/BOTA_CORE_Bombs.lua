-- Weapon definitions (native Recoil tags; converted from BOTA_CORE_Bombs.TDF)

return {
	core_shadow_bomb = {
		-- used by units
		-- CORE_T1_AIR_Shadow
		-- type
		weapontype = "AircraftBomb",
		rgbcolor = "1.000 0.000 0.000",
		-- visuals
		model = "BOTA_Bomb-CORE_Shadow",
		explosiongenerator = "custom:CORBOMB_Expl",
		-- sounds
		soundstart = "bombrel",
		soundhit = "xplomed2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		-- stats
		range = 1280,
		reloadtime = 0.14,
		areaofeffect = 48,
		craterareaofeffect = 72,
		damage = {
			default = 165,  -- 150
		},
	},
	core_hurricane_bomb = {
		-- used by units
		-- CORE_T2_AIR_Hurricane
		-- type
		weapontype = "AircraftBomb",
		rgbcolor = "1.000 0.000 0.000",
		-- visuals
		model = "BOTA_Bomb-CORE_Hurricane",
		explosiongenerator = "custom:CORBOMB_Expl",
		-- sounds
		soundstart = "bombrel",
		soundhit = "xplomed2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		-- stats
		range = 1280,
		reloadtime = 0.13,
		areaofeffect = 64,
		craterareaofeffect = 96,
		damage = {
			default = 217,
		},
	},
}
