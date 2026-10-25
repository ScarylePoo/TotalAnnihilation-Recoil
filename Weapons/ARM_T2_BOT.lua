-- Weapon definitions (native Recoil tags; converted from ARM_T2_BOT.TDF)

return {
	gauss = {
		name = "Gauss Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		turret = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		range = 680,
		reloadtime = 1.25,
		weaponvelocity = 600,
		areaofeffect = 12,
		craterareaofeffect = 18,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		explosiongenerator = "custom:GAUSS_Expl",
		damage = {
			default = 120,
		},
	},
	armmav_weapon = {
		name = "Gauss Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 580,
		reloadtime = 0.8,
		weaponvelocity = 680,
		areaofeffect = 8,
		craterareaofeffect = 12,
		soundstart = "Mavgun2",
		soundhit = "xplomed2",
		tolerance = 300,
		damage = {
			default = 320,
		},
	},
	armsnipe_weapon = {
		name = "Annihilator Weapon",
		weapontype = "LaserCannon",
		rgbcolor = "0.000 0.012 1.000",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 950,  -- 600
		reloadtime = 20,
		energypershot = 1500,
		weaponvelocity = 1200,  -- 1000
		areaofeffect = 8,
		craterareaofeffect = 12,
		soundstart = "annigun1",
		soundhit = "xplolrg1",
		firestarter = 90,
		-- PURPLE
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
		name = "Lightning Gun",
		weapontype = "LightningCannon",
		rgbcolor = "0.000 1.000 0.776",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 310,  -- 180//280//240
		reloadtime = 1.85,  -- 1.45
		weaponvelocity = 400,
		areaofeffect = 8,
		craterareaofeffect = 12,
		duration = 10,
		soundtrigger = 1,
		soundstart = "lghthvy1",
		soundhit = "lashit",
		firestarter = 50,
		-- Yellow
		explosiongenerator = "custom:LIGHTNING",
		damage = {
			default = 240,  -- 180//320
		},
	},
}
