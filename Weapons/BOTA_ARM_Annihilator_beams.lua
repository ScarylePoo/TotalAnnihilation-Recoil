-- Weapon definitions (converted from BOTA_ARM_Annihilator_beams.TDF)

return {
	annihilator_beam = {
		-- used by units
		-- ARM_T2_DEF_Annihilator
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
		-- sounds
		soundstart = "annigun1",
		soundhit = "xplolrg1",
		-- behaviour
		avoidfriendly = 1,
		collidefriendly = 1,
		firestarter = 90,
		beamtime = 1.0,
		targetmoveerror = 0.3,
		tolerance = 500,
		weaponvelocity = 1000,
		-- costs
		energypershot = 2000,
		-- stats
		range = 1200,  -- TA 3.1c (was 1480)
		reloadtime = 5,  -- TA 3.1c (was 6)
		areaofeffect = 8,  -- TA 3.1c (was 42)
		minintensity = 1,
		damage = {
			default = 2500,  -- TA 3.1c (was 3200)
		},
	},
	penetrator_annihilator_beam = {
		-- used by units
		-- ARM_T2_VEH_Penetrator
		-- type
		weapontype = "LaserCannon",  -- was BeamLaser: TA had no continuous beams (user decision)
		turret = 1,
		-- visuals
		laserflaresize = 10,
		thickness = 10,
		rgbcolor = "0.1 0.1 0.9",  -- blueish
		corethickness = 0.4,
		rgbcolor2 = "0.7 0.7 0.9",  -- white with a touch of blue
		-- sounds
		soundstart = "annigun1",
		soundhit = "xplolrg1",
		-- behaviour
		avoidfriendly = 1,
		collidefriendly = 1,
		firestarter = 90,
		targetmoveerror = 0.3,
		tolerance = 500,
		weaponvelocity = 1000,
		-- costs
		energypershot = 1500,
		-- stats
		range = 700,  -- TA 3.1c (was 1250)
		reloadtime = 6,  -- TA 3.1c (was 7)
		areaofeffect = 8,  -- TA 3.1c (was 32)
		accuracy = 100,  -- TA 3.1c (was unset)
		damage = {
			default = 1300,  -- TA 3.1c (was 2000)
		},
	},
}
