-- Weapon definitions (native Recoil tags; converted from BOTA_CORE_Flaks.TDF)

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
		name = "Flak Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		canattackground = 0,
		range = 1000,  -- 750
		reloadtime = 0.7,
		weapontimer = 1,
		weaponvelocity = 950,
		areaofeffect = 225,  -- 125
		craterareaofeffect = 337.5,
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
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
		name = "Flak Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		turret = 1,
		canattackground = 0,
		range = 1000,  -- 750
		reloadtime = 0.7,
		weapontimer = 1,
		weaponvelocity = 950,
		areaofeffect = 225,  -- 125
		craterareaofeffect = 337.5,
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
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
		name = "Flak Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		canattackground = 0,
		turret = 1,
		range = 930,  -- 720
		reloadtime = 0.95,
		weapontimer = 1,
		weaponvelocity = 900,
		areaofeffect = 200,  -- 110
		craterareaofeffect = 300,
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
		explosiongenerator = "custom:FLAK_BURST_Expl",
		damage = {
			default = 170,  -- 130
		},
	},
}
