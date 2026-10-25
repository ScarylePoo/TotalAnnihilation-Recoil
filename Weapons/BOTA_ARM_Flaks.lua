-- Weapon definitions (native Recoil tags; converted from BOTA_ARM_Flaks.TDF)

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
		name = "Flak Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		turret = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		canattackground = 0,
		range = 900,  -- 700
		reloadtime = 0.6,
		weapontimer = 1,
		weaponvelocity = 950,
		areaofeffect = 220,  -- 120
		craterareaofeffect = 330,
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
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
	armyork_gun = {
		-- used by units
		-- ARM_T2_VEH_Phalanx
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
		avoidfriendly = 0,
		collidefriendly = 0,
		canattackground = 0,
		range = 880,  -- 680
		reloadtime = 0.55,
		weapontimer = 1,
		weaponvelocity = 900,
		areaofeffect = 190,  -- 105
		craterareaofeffect = 285,
		edgeeffectiveness = 0.90,
		soundstart = "canlite2",
		soundhit = "flakhit",  -- xplomed2
		accuracy = 1000,
		tolerance = 767,
		burnblow = 1,
		explosiongenerator = "custom:FLAK_BURST_Expl",
		damage = {
			default = 168,  -- 128
		},
	},
}
