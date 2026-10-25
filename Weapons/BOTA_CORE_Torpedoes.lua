-- Weapon definitions (native Recoil tags; converted from BOTA_CORE_Torpedoes.TDF)

return {
	core_torpedo = {
		-- used by units
		-- CORE_T1_SEA_Snake
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		turnrate = 4000,
		-- stats
		range = 500,
		reloadtime = 4,
		areaofeffect = 16,
		craterareaofeffect = 24,
		damage = {
			default = 546,
			-- subkillers=191;
		},
	},
	coax_torpedo = {
		-- used by units
		-- CORE_T1_SEADEF_TorpedoLauncher
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		turnrate = 3000,
		-- stats
		range = 500,
		reloadtime = 2.6,
		areaofeffect = 16,
		craterareaofeffect = 24,
		damage = {
			default = 400,
		},
	},
	corseap_weapon1 = {
		-- used by units
		-- CORE_T1_SEAPL_Typhoon
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		weaponvelocity = 2,
		startvelocity = 2,
		weaponacceleration = 15,
		turnrate = 15000,
		-- stats
		range = 480,
		reloadtime = 6,
		areaofeffect = 16,
		craterareaofeffect = 24,
		burst = 2,
		damage = {
			default = 600,
		},
	},
	corseap_weapon2 = {
		-- used by units
		-- CORE_T1_SEAPL_Typhoon
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		weaponvelocity = 2,
		startvelocity = 2,
		weaponacceleration = 15,
		turnrate = 15000,
		-- stats
		range = 480,
		reloadtime = 6,
		areaofeffect = 16,
		craterareaofeffect = 24,
		damage = {
			default = 400,
		},
	},
	corair_torpedo = {
		-- used by units
		-- CORE_T2_AIR_Titan
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		craterareaofeffect = 24,
		damage = {
			default = 780,
			-- subs=1100;
		},
	},
	corssub_weapon = {
		-- used by units
		-- CORE_T2_SEA_Leviathan
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 750,
		reloadtime = 5.8,
		areaofeffect = 5,
		craterareaofeffect = 7.5,
		damage = {
			default = 812,
			-- subkillers=300;
			-- armatl=150;
			-- coratl=150;
			-- armtl=250;
			-- cortl=250;
			-- armsubk=80;
			-- corshark=90;
		},
	},
	corsmart_torpedo = {
		-- used by units
		-- CORE_T2_SEA_Shark
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 550,
		reloadtime = 2.28,
		areaofeffect = 16,
		craterareaofeffect = 24,
		damage = {
			default = 210,
			-- subs=1100;//800
		},
	},
	coratl_torpedo = {
		-- used by units
		-- CORE_T2_SEADEF_AdvancedTorpedoLauncher
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 900,
		reloadtime = 4.4,
		areaofeffect = 16,
		craterareaofeffect = 24,
		damage = {
			default = 1000,
		},
	},
}
