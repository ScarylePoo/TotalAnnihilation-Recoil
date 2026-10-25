-- Weapon definitions (converted from BOTA_ARM_Flaks.TDF)

return {
	armflak_gun = {
		-- used by units
		-- ARM_T2_DEF_Flakker
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 42,
		name = "Flak Cannon",
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		canattackground = 0,
		range = 900,  -- 700
		reloadtime = 0.6,
		weapontimer = 1,
		weaponvelocity = 950,
		areaofeffect = 220,  -- 120
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		minbarrelangle = -24,
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		color = 1,
		startsmoke = 1,
		explosiongenerator = "custom:FLAK_BURST_Expl",
		damage = {
			default = 180,
			planes = 180,  -- armor group needed only for defense range
		},
	},
	armaas_weapon3 = {
		-- used by units
		-- ARM_T2_SEA_Archer
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 79,
		name = "Flak Cannon",
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		canattackground = 0,
		range = 1000,  -- 750
		reloadtime = 0.7,
		weapontimer = 1,
		weaponvelocity = 950,
		areaofeffect = 225,  -- 125
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		minbarrelangle = -24,
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		color = 1,
		startsmoke = 1,
		explosiongenerator = "custom:FLAK_BURST_Expl",
		damage = {
			default = 186,  -- 146
		},
	},
	armyork_gun = {
		-- used by units
		-- ARM_T2_VEH_Phalanx
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 116,
		name = "Flak Cannon",
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		canattackground = 0,
		range = 880,  -- 680
		reloadtime = 0.55,
		weapontimer = 1,
		weaponvelocity = 900,
		areaofeffect = 190,  -- 105
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		minbarrelangle = -24,
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		color = 1,
		startsmoke = 1,
		explosiongenerator = "custom:FLAK_BURST_Expl",
		damage = {
			default = 168,  -- 128
		},
	},
}
