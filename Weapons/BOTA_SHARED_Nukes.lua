-- Weapon definitions (converted from BOTA_SHARED_Nukes.TDF)

return {
	nuclear_missile = {
		-- used by units
		-- ARM_T2_DEF_Retaliator
		-- CORE_T2_DEF_Silencer
		-- type
		weapontype = "StarburstLauncher",
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
		energypershot = 180000,  -- TA 3.1c (was 190000)
		metalpershot = 2000,  -- TA 3.1c (was 1900)
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
		reloadtime = 180,  -- TA 3.1c (was 190)
		areaofeffect = 512,  -- TA 3.1c (was 1024)
		edgeeffectiveness = 0.25,  -- TA 3.1c (was 0.3)
		damage = {
			default = 5500,  -- TA 3.1c (was 10000)
			arm_commander_armor = 2900,
			core_commander_armor = 2900,
		},
	},
	anti_nuclear_missile = {
		-- used by units
		-- ARM_T2_DEF_Protector
		-- CORE_T2_DEF_FortitudeMissileDefense
		-- type
		weapontype = "StarburstLauncher",
		stockpile = 1,
		interceptor = 1,
		coverage = 2000,  -- TA 3.1c (was 1100)
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
		energypershot = 10000,  -- TA 3.1c (was 20000)
		metalpershot = 200,
		-- stats
		range = 32000,
		reloadtime = 120,  -- TA 3.1c (was 100)
		areaofeffect = 96,
		damage = {
			default = 500,
		},
	},
	cormabm_weapon = {
		-- TA 3.1c weapon cormabm_weapon (BOTA used mobile_anti_nuclear_missile for it as well)
		-- used by units
		-- CORE_T2_VEH_Hedgehog
		-- type
		weapontype = "StarburstLauncher",
		stockpile = 1,
		interceptor = 1,
		coverage = 2000,  -- TA 3.1c (was 600)
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
		energypershot = 10000,  -- TA 3.1c (was 20000)
		metalpershot = 200,
		-- stats
		range = 22000,  -- TA 3.1c (was 25000)
		reloadtime = 120,  -- TA 3.1c (was 100)
		areaofeffect = 96,
		damage = {
			default = 500,
		},
	},
	armscab_weapon = {
		-- TA 3.1c weapon armscab_weapon (BOTA used mobile_anti_nuclear_missile for it as well)
		-- used by units
		-- ARM_T2_VEH_Scarab
		-- type
		weapontype = "StarburstLauncher",
		stockpile = 1,
		interceptor = 1,
		coverage = 2000,  -- TA 3.1c (was 600)
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
		energypershot = 10000,  -- TA 3.1c (was 20000)
		metalpershot = 200,
		-- stats
		range = 27000,  -- TA 3.1c (was 25000)
		reloadtime = 120,  -- TA 3.1c (was 100)
		areaofeffect = 96,
		damage = {
			default = 500,
		},
	},
	stunner_missile = {
		-- used by units
		-- ARM_T2_DEF_Stunner
		-- type
		weapontype = "StarburstLauncher",
		stockpile = 1,
		targetable = 1,
		commandfire = 1,
		-- visuals
		model = "BOTA_Stunner_Missile",
		smoketrail = 1,
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
		weapontimer = 5,  -- TA 3.1c (was 4.2)
		weaponvelocity = 350,  -- TA 3.1c (was 500)
		weaponacceleration = 50,  -- TA 3.1c (was 200)
		flighttime = 400,
		turnrate = 32768,
		-- costs
		energypershot = 18000,  -- TA 3.1c (was 40000)
		metalpershot = 1000,  -- TA 3.1c (was 400)
		-- stats
		range = 32000,
		reloadtime = 130,  -- TA 3.1c (was 150)
		areaofeffect = 512,  -- TA 3.1c (was 768)
		edgeeffectiveness = 0.8,  -- TA 3.1c (was 0.3)
		damage = {
			default = 1,  -- TA 3.1c (was 80000)
			anti_nukes = 1,
			core_aircraft = 1800,
			core_commander_armor = 100,
			core_mobile = 1800,
			core_t1_def_mine1_armor = 1800,
			core_t1_def_mine2_armor = 1800,
			core_t1_def_mine3_armor = 1800,
			core_t1_def_mine4_armor = 1800,
			core_t1_def_mine5_armor = 1800,
			core_t1_sea_snake_armor = 1800,
			core_t1_seadef_torpedolauncher_armor = 1800,
			core_t2_bot_pyro_armor = 1800,
			core_t2_bot_sumo_armor = 1800,
			core_t2_bot_thecan_armor = 1800,
			core_t2_sea_shark_armor = 1800,
			core_t2_seadef_advancedtorpedolauncher_armor = 1800,
			core_t3_bot_krogoth_armor = 1800,
		},
	},
	neutron_missile = {
		-- used by units
		-- CORE_T2_DEF_Neutron
		-- type
		weapontype = "StarburstLauncher",
		stockpile = 1,
		targetable = 1,
		commandfire = 1,
		-- visuals
		model = "BOTA_Neutron_Missile",
		smoketrail = 1,
		-- sounds
		soundstart = "misicbm1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		tolerance = 4000,
		weapontimer = 5,  -- TA 3.1c (was 4.2)
		weaponvelocity = 350,  -- TA 3.1c (was 500)
		weaponacceleration = 50,  -- TA 3.1c (was 250)
		flighttime = 400,
		turnrate = 32768,
		-- costs
		energypershot = 150000,  -- TA 3.1c (was 70000)
		metalpershot = 1800,  -- TA 3.1c (was 700)
		-- stats
		range = 32000,
		reloadtime = 180,  -- TA 3.1c (was 170)
		areaofeffect = 362,  -- TA 3.1c (was 512)
		edgeeffectiveness = 0.25,  -- TA 3.1c (was 0.3)
		damage = {
			default = 1,  -- TA 3.1c (was 2000)
			arm_aircraft = 2000,
			arm_commander_armor = 1500,
			arm_mobile = 2000,
			arm_t1_bot_peewee_armor = 2000,
			arm_t1_bot_warrior_armor = 2000,
			arm_t1_sea_lurker_armor = 2000,
			arm_t1_veh_flash_armor = 2000,
			arm_t2_sea_piranha_armor = 2000,
		},
	},
}
