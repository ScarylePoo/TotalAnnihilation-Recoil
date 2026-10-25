-- Weapon definitions (converted from ARM_T2_BOT.TDF)

return {
	gauss = {
		id = 60,
		name = "Gauss Cannon",
		rendertype = 4,
		lineofsight = 1,
		turret = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		minbarrelangle = -15,
		range = 680,
		reloadtime = 1.25,
		weaponvelocity = 600,
		areaofeffect = 12,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		explosiongenerator = "custom:GAUSS_Expl",
		startsmoke = 1,
		damage = {
			default = 120,
		},
	},
	armmav_weapon = {
		id = 190,
		name = "Gauss Cannon",
		rendertype = 4,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -15,
		range = 580,
		reloadtime = 0.8,
		weaponvelocity = 680,
		areaofeffect = 8,
		soundstart = "Mavgun2",
		soundhit = "xplomed2",
		tolerance = 300,
		explosiongaf = "fx",
		explosionart = "explode5",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom1",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplashsm",
		startsmoke = 1,
		damage = {
			default = 320,
		},
	},
	armsnipe_weapon = {
		id = 160,
		name = "Annihilator Weapon",
		rendertype = 0,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 950,  -- 600
		reloadtime = 20,
		energypershot = 1500,
		weaponvelocity = 1200,  -- 1000
		areaofeffect = 8,
		soundstart = "annigun1",
		soundhit = "xplolrg1",
		firestarter = 90,
		beamweapon = 1,
		color = 144,
		-- PURPLE
		color2 = 217,
		explosiongaf = "fx",
		explosionart = "explode5",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom1",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplashsm",
		damage = {
			default = 1800,  -- 1230//2460//1500//882
			-- CoreSumoKrog=4860;//2460//4860//2859
			-- corkrog=2460;
			-- armcom=615;
			-- corcom=820;
			-- corcan=2810;
			-- corsumo=5000;
		},
		cratermult = 0,
		craterboost = 0,
		impulsefactor = 0,
		impulseboost = 0,
		leadlimit = 0,
		leadbonus = 2,
		heightboostfactor = 0,
	},
	lightning = {
		id = 26,
		name = "Lightning Gun",
		rendertype = 7,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 310,  -- 180//280//240
		reloadtime = 1.85,  -- 1.45
		weaponvelocity = 400,
		areaofeffect = 8,
		duration = 10,
		soundtrigger = 1,
		soundstart = "lghthvy1",
		soundhit = "lashit",
		firestarter = 50,
		beamweapon = 1,
		color = 118,
		-- Yellow
		color2 = 240,  -- 196
		explosiongenerator = "custom:LIGHTNING",
		startsmoke = 1,
		damage = {
			default = 240,  -- 180//320
		},
	},
}
