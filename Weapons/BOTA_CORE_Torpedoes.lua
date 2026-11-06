-- Weapon definitions (converted from BOTA_CORE_Torpedoes.TDF)

return {
	core_torpedo = {
		-- used by units
		-- CORE_T1_SEA_Snake
		-- type
		weapontype = "TorpedoLauncher",
		turret = 0,
		tolerance = 32767,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "torpedo2",
		soundhit = "xplodep3",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 3,
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 500,  -- TA 3.1c (was 4000)
		-- stats
		range = 400,  -- TA 3.1c (was 500)
		reloadtime = 2.71,  -- TA 3.1c (was 4)
		areaofeffect = 16,
		damage = {
			default = 370,  -- TA 3.1c (was 546)
			arm_t2_sea_piranha_armor = 130,
			core_t2_sea_shark_armor = 130,
		},
	},
	coax_torpedo = {
		-- used by units
		-- ARM_T1_SEADEF_TorpedoLauncher
		-- CORE_T1_SEADEF_TorpedoLauncher
		-- type
		weapontype = "TorpedoLauncher",
		turret = 1,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "torpedo1",
		soundhit = "xplodep2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 3,
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 500,  -- TA 3.1c (was 3000)
		-- stats
		range = 400,  -- TA 3.1c (was 500)
		reloadtime = 2.6,
		areaofeffect = 16,
		damage = {
			default = 400,
		},
	},
	corseap_weapon1 = {
		-- used by units
		-- CORE_T1_SEAPL_Typhoon
		-- type
		weapontype = "TorpedoLauncher",
		turret = 0,
		tolerance = 12000,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "bombrel",
		soundhit = "xplodep2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 5,
		weaponvelocity = 100,  -- TA 3.1c (was 2)
		startvelocity = 100,  -- TA 3.1c (was 2)
		weaponacceleration = 15,
		turnrate = 15000,
		-- stats
		range = 300,  -- TA 3.1c (was 480)
		reloadtime = 6,
		areaofeffect = 16,
		burst = 2,
		bursttime = 0.35,
		damage = {
			default = 400,  -- TA 3.1c (was 600)
		},
	},
	corseap_weapon2 = {
		-- used by units
		-- CORE_T1_SEAPL_Typhoon
		-- type
		weapontype = "TorpedoLauncher",
		turret = 0,
		tolerance = 12000,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "bombrel",
		soundhit = "xplodep2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 5,
		weaponvelocity = 100,  -- TA 3.1c (was 2)
		startvelocity = 100,  -- TA 3.1c (was 2)
		weaponacceleration = 15,
		turnrate = 15000,
		-- stats
		range = 300,  -- TA 3.1c (was 480)
		reloadtime = 6,
		areaofeffect = 16,
		damage = {
			default = 400,
		},
	},
	corair_torpedo = {
		-- used by units
		-- CORE_T2_AIR_Titan
		-- type
		weapontype = "TorpedoLauncher",
		turret = 0,
		tolerance = 6000,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "bombrel",
		soundhit = "xplodep2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 5,
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 10000,
		-- stats
		range = 400,
		reloadtime = 9,
		areaofeffect = 16,
		damage = {
			default = 780,
		},
	},
	corssub_weapon = {
		-- used by units
		-- CORE_T2_SEA_Leviathan
		-- type
		weapontype = "TorpedoLauncher",
		turret = 0,
		tolerance = 37152,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "torpedo2",
		soundhit = "xplodep3",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 3,
		weaponvelocity = 100,
		startvelocity = 60,
		weaponacceleration = 15,
		turnrate = 38000,
		-- stats
		range = 500,  -- TA 3.1c (was 750)
		reloadtime = 5.8,
		areaofeffect = 5,
		damage = {
			default = 812,
			arm_t1_seadef_torpedolauncher_armor = 250,
			arm_t2_sea_piranha_armor = 80,
			arm_t2_seadef_advancedtorpedolauncher_armor = 150,
			core_t1_seadef_torpedolauncher_armor = 250,
			core_t2_sea_shark_armor = 90,
			core_t2_seadef_advancedtorpedolauncher_armor = 150,
		},
	},
	corsmart_torpedo = {
		-- used by units
		-- CORE_T2_SEA_Shark
		-- type
		weapontype = "TorpedoLauncher",
		turret = 0,
		tolerance = 32767,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_Torpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "torpedo2",
		soundhit = "xplodep3",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 3,
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 10000,
		-- stats
		range = 375,  -- TA 3.1c (was 550)
		reloadtime = 2.28,
		areaofeffect = 16,
		damage = {
			default = 210,
			arm_t1_sea_lurker_armor = 600,
			core_t1_sea_snake_armor = 600,
		},
	},
	coratl_torpedo = {
		-- used by units
		-- CORE_T2_SEADEF_AdvancedTorpedoLauncher
		-- type
		weapontype = "TorpedoLauncher",
		turret = 1,
		tolerance = 2767,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_AdvancedTorpedo",
		explosiongenerator = "custom:KERSPLUNK",
		-- sounds
		soundstart = "torpedo1",
		soundhit = "xplodep1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 3,
		weaponvelocity = 85,
		startvelocity = 50,
		weaponacceleration = 10,
		turnrate = 30500,
		-- stats
		range = 600,  -- TA 3.1c (was 900)
		reloadtime = 4.4,
		areaofeffect = 16,
		damage = {
			default = 1000,
		},
	},
}
