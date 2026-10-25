-- Weapon definitions (native Recoil tags; converted from BOTA_SHARED_Nukes.TDF)

return {
	nuclear_missile = {
		-- used by units
		-- ARM_T2_DEF_Retaliator
		-- CORE_T2_DEF_Silencer
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		stockpile = 1,
		targetable = 1,
		commandfire = 1,
		-- visuals
		model = "BOTA_Nuclear_Missile",
		smoketrail = 1,
		-- sounds
		soundstart = "misicbm1",
		soundhit = "xplomed4",
		-- costs
		energypershot = 190000,
		metalpershot = 1900,
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		tolerance = 4000,
		weapontimer = 5,
		weaponvelocity = 350,
		weaponacceleration = 50,
		flighttime = 400,
		turnrate = 32768,
		-- stats
		range = 32000,
		reloadtime = 2,
		stockpiletime = 190,
		areaofeffect = 1024,
		craterareaofeffect = 1536,
		edgeeffectiveness = 0.3,
		damage = {
			default = 10000,
		},
	},
	anti_nuclear_missile = {
		-- used by units
		-- ARM_T2_DEF_Protector
		-- CORE_T2_DEF_FortitudeMissileDefense
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		stockpile = 1,
		interceptor = 1,
		coverage = 1100,
		tracks = 1,
		-- visuals
		model = "BOTA_Anti_Nuclear_Missile",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		tolerance = 4000,
		weapontimer = 4,
		weaponvelocity = 800,
		weaponacceleration = 60,
		flighttime = 60,
		turnrate = 32768,
		-- costs
		energypershot = 20000,
		metalpershot = 200,
		-- stats
		range = 32000,
		reloadtime = 2,
		stockpiletime = 100,
		areaofeffect = 96,
		craterareaofeffect = 144,
		damage = {
			default = 500,
		},
	},
	mobile_anti_nuclear_missile = {
		-- used by units
		-- ARM_T2_VEH_Scarab
		-- CORE_T2_VEH_Hedgehog
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		stockpile = 1,
		interceptor = 1,
		coverage = 600,
		tracks = 1,
		-- visuals
		model = "BOTA_Anti_Nuclear_Missile",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		tolerance = 4000,
		weapontimer = 4,
		weaponvelocity = 800,
		weaponacceleration = 60,
		flighttime = 60,
		turnrate = 32768,
		-- costs
		energypershot = 20000,
		metalpershot = 200,
		-- stats
		range = 25000,
		reloadtime = 2,
		stockpiletime = 100,
		areaofeffect = 96,
		craterareaofeffect = 144,
		damage = {
			default = 500,
		},
	},
	stunner_missile = {
		-- used by units
		-- ARM_T2_DEF_Stunner
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		stockpile = 1,
		targetable = 1,
		commandfire = 1,
		-- visuals
		model = "BOTA_Stunner_Missile",
		smoketrail = 1,
		explosiongenerator = "custom:STUNNER_Expl",
		-- sounds
		soundstart = "misicbm1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 100,
		paralyzer = 1,
		paralyzetime = 30,
		tolerance = 4000,
		weapontimer = 4.2,
		weaponvelocity = 500,
		weaponacceleration = 200,
		flighttime = 400,
		turnrate = 32768,
		-- costs
		energypershot = 40000,
		metalpershot = 400,
		-- stats
		range = 32000,
		reloadtime = 2,
		stockpiletime = 150,
		areaofeffect = 768,
		craterareaofeffect = 1152,
		edgeeffectiveness = 0.3,
		damage = {
			default = 80000,
		},
	},
	neutron_missile = {
		-- used by units
		-- CORE_T2_DEF_Neutron
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		stockpile = 1,
		targetable = 1,
		commandfire = 1,
		-- visuals
		model = "BOTA_Neutron_Missile",
		smoketrail = 1,
		explosiongenerator = "custom:NEUTRON_Expl",
		-- sounds
		soundstart = "misicbm1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		tolerance = 4000,
		weapontimer = 4.2,
		weaponvelocity = 500,
		weaponacceleration = 250,
		flighttime = 400,
		turnrate = 32768,
		-- costs
		energypershot = 70000,
		metalpershot = 700,
		-- stats
		range = 32000,
		reloadtime = 2,
		stockpiletime = 170,
		areaofeffect = 512,
		craterareaofeffect = 768,
		edgeeffectiveness = 0.3,
		damage = {
			default = 2000,
		},
	},
}
