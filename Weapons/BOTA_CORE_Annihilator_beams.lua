-- Weapon definitions (converted from BOTA_CORE_Annihilator_beams.TDF)

return {
	doomsday_annihilator_beam = {
		-- used by units
		-- CORE_T2_DEF_DoomsdayMachine
		-- type
		weapontype = "LaserCannon",  -- was BeamLaser: TA had no continuous beams (user decision)
		turret = 1,
		-- visuals
		laserflaresize = 10,
		thickness = 20,
		rgbcolor = "0.1 0.1 0.9",  -- blueish
		corethickness = 0.4,
		rgbcolor2 = "0.7 0.7 0.9",  -- white with a touch of blue
		-- sounds
		soundstart = "annigun1",
		soundhit = "xplosml3",
		-- behaviour
		avoidfriendly = 1,
		collidefriendly = 1,
		firestarter = 90,
		targetmoveerror = 0.3,
		tolerance = 500,
		weaponvelocity = 1000,
		-- costs
		energypershot = 800,
		-- stats
		range = 600,  -- TA 3.1c (was 950)
		reloadtime = 8,
		areaofeffect = 8,  -- TA 3.1c (was 32)
		damage = {
			default = 2500,
		},
	},
	krogoth_annihilator_beam = {
		-- used by units
		-- CORE_T3_BOT_Krogoth
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
		energypershot = 2000,
		-- stats
		range = 700,  -- TA 3.1c (was 1000)
		reloadtime = 4,
		areaofeffect = 8,  -- TA 3.1c (was 32)
		damage = {
			default = 2500,
		},
	},
}
