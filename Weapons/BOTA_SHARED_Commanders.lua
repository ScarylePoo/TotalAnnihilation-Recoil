-- Weapon definitions (converted from BOTA_SHARED_Commanders.TDF)

return {
	commander_laser = {
		-- used by units
		-- ARM_Commander
		-- ARM_T2_BOT_DecoyCommander
		-- CORE_Commander
		-- CORE_T2_BOT_DecoyCommander
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.05,
		hardstop = 1,
		thickness = 20,
		rgbcolor = "0.8 0 0",  -- reddish
		corethickness = 0.3,
		rgbcolor2 = "0.8 0.8 0",  -- yellowish
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfir1",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weaponvelocity = 700,
		-- stats
		range = 290,
		reloadtime = 0.85,
		areaofeffect = 16,
		damage = {
			default = 95,
		},
	},
	disintegrator = {
		-- used by units
		-- ARM_Commander
		-- CORE_Commander
		-- type
		-- weapontype detected from the name as Dgun
		turret = 1,
		commandfire = 1,
		-- visuals
		model = "BOTA_Disintegrator_Gun",
		-- sounds
		soundtrigger = 1,
		soundstart = "disigun1",
		soundhit = "xplomas2",
		-- costs
		energypershot = 400,
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 70,
		noexplode = 1,
		weaponvelocity = 242,
		-- stats
		range = 290,
		reloadtime = 1.2,
		areaofeffect = 48,
		damage = {
			default = 30000,
		},
	},
	commander_explosion = {
		-- type
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		-- visuals
		explosiongenerator = "custom:ARGHNUKE_FX",
		-- sounds
		soundstart = "largegun",
		soundhit = "xplonuk4",
		-- behaviour
		weaponvelocity = 250,
		-- stats
		range = 380,
		reloadtime = 3.6,
		areaofeffect = 950,
		edgeeffectiveness = 0.75,
		damage = {
			default = 9999,
		},
	},
}
