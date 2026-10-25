-- Weapon definitions (converted from BOTA_CORE_Flaks.TDF)

return {
	corflak_gun = {
		-- used by units
		-- CORE_T2_DEF_Cobra
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 43,
		name = "Flak Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
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
			default = 186,
			planes = 186,  -- armor group needed only for defense range
		},
	},
	corarch_weapon3 = {
		-- used by units
		-- CORE_T2_SEA_Shredder
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 180,
		name = "Flak Cannon",
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		toairweapon = 1,
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
	corsent_gun = {
		-- used by units
		-- CORE_T2_VEH_Copperhead
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 133,
		name = "Flak Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		canattackground = 0,
		turret = 1,
		range = 930,  -- 720
		reloadtime = 0.95,
		weapontimer = 1,
		weaponvelocity = 900,
		areaofeffect = 200,  -- 110
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
			default = 170,  -- 130
		},
	},
}
