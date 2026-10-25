-- Weapon definitions (converted from BOTA_ARM_Torpedoes.TDF)

return {
	arm_torpedo = {
		-- used by units
		-- ARM_T1_SEA_Lurker
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
		soundstart = "torpedo1",
		soundhit = "xplodep1",
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
		damage = {
			default = 518,
			-- subkillers=170;
		},
	},
	coax_torpedo = {
		-- used by units
		-- ARM_T1_SEADEF_TorpedoLauncher
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
		turnrate = 3000,
		-- stats
		range = 500,
		reloadtime = 2.6,
		areaofeffect = 16,
		damage = {
			default = 400,
		},
	},
	armseap_weapon1 = {
		-- used by units
		-- ARM_T1_SEAPL_Albatross
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
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 15000,
		-- stats
		range = 480,
		reloadtime = 6,
		burst = 2,
		bursttime = 0.35,
		areaofeffect = 16,
		damage = {
			default = 600,
		},
	},
	armseap_weapon2 = {
		-- used by units
		-- ARM_T1_SEAPL_Albatross
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
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 15000,
		-- stats
		range = 480,
		reloadtime = 6,
		areaofeffect = 16,
		damage = {
			default = 400,
		},
	},
	armair_torpedo = {
		-- used by units
		-- ARM_T2_AIR_Lancet
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
		reloadtime = 8.5,
		areaofeffect = 16,
		damage = {
			default = 750,
			-- subs=1000;
		},
	},
	armsmart_torpedo = {
		-- used by units
		-- ARM_T2_SEA_Piranha
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
		soundstart = "torpedo1",
		soundhit = "xplodep1",
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
		reloadtime = 2.3,
		areaofeffect = 16,
		damage = {
			default = 200,
			-- subs=1060;//760
		},
	},
	armatl_torpedo = {
		-- used by units
		-- ARM_T2_SEADEF_AdvancedTorpedoLauncher
		-- type
		weapontype = "TorpedoLauncher",
		turret = 1,
		tolerance = 1167,
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
		weaponvelocity = 90,
		startvelocity = 60,
		weaponacceleration = 20,
		turnrate = 45500,
		-- stats
		range = 970,
		reloadtime = 4.5,
		areaofeffect = 16,
		damage = {
			default = 1000,
		},
	},
}
