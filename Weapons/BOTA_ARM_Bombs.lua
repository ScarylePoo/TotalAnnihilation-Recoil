-- Weapon definitions (converted from BOTA_ARM_Bombs.TDF)

return {
	arm_thunder_bomb = {
		-- used by units
		-- ARM_T1_AIR_Thunder
		-- type
		weapontype = "AircraftBomb",
		-- visuals
		model = "BOTA_Bomb-ARM_Shadow",
		explosiongenerator = "custom:ARMBOMB_Expl",
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
		damage = {
			default = 173,
		},
	},
	arm_phoenix_bomb = {
		-- used by units
		-- ARM_T2_AIR_Phoenix
		-- type
		weapontype = "AircraftBomb",
		-- visuals
		model = "BOTA_Bomb-ARM_Phoenix",
		explosiongenerator = "custom:ARMBOMB_Expl",
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
		damage = {
			default = 215,
		},
	},
}
