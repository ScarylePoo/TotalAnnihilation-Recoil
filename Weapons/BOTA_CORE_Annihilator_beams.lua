-- Weapon definitions (converted from BOTA_CORE_Annihilator_beams.TDF)

return {
	doomsday_annihilator_beam = {
		-- used by units
		-- type
		weapontype = "BeamLaser",
		turret = 1,
		-- visuals
		largebeamlaser = 1,
		pulsespeed = 10,
		scrollspeed = 1,
		beamttl = 30,
		tilelength = 100,
		beamburst = 1,
		laserflaresize = 10,
		thickness = 20,
		rgbcolor = "0.1 0.1 0.9",  -- blueish
		corethickness = 0.4,
		rgbcolor2 = "0.7 0.7 0.9",  -- white with a touch of blue
		explosiongenerator = "custom:FLASH1blue_LONG",
		-- sounds
		soundstart = "annigun1",
		soundhit = "xplosml3",
		-- behaviour
		avoidfriendly = 1,
		collidefriendly = 1,
		firestarter = 90,
		beamtime = 1.0,
		targetmoveerror = 0.3,
		tolerance = 500,
		weaponvelocity = 1000,
		-- costs
		energypershot = 800,
		-- stats
		range = 950,
		reloadtime = 8,
		areaofeffect = 32,
		minintensity = 1,
		damage = {
			default = 2500,
		},
	},
	krogoth_annihilator_beam = {
		-- used by units
		-- type
		weapontype = "BeamLaser",
		turret = 1,
		-- visuals
		largebeamlaser = 1,
		pulsespeed = 10,
		scrollspeed = 1,
		beamttl = 30,
		tilelength = 100,
		beamburst = 1,
		laserflaresize = 10,
		thickness = 10,
		rgbcolor = "0.1 0.1 0.9",  -- blueish
		corethickness = 0.4,
		rgbcolor2 = "0.7 0.7 0.9",  -- white with a touch of blue
		explosiongenerator = "custom:FLASH1blue_LONG",
		-- sounds
		soundstart = "annigun1",
		soundhit = "xplolrg1",
		-- behaviour
		avoidfriendly = 1,
		collidefriendly = 1,
		firestarter = 90,
		beamtime = 0.3,
		targetmoveerror = 0.3,
		tolerance = 500,
		weaponvelocity = 1000,
		-- costs
		energypershot = 2000,
		-- stats
		range = 1000,
		reloadtime = 4,
		areaofeffect = 32,
		minintensity = 1,
		damage = {
			default = 2500,
		},
	},
}
