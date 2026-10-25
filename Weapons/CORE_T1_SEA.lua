-- Weapon definitions (converted from CORE_T1_SEA.TDF)

return {
	core_roy = {
		id = 65,
		name = "Heavy Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -25,
		range = 950,  -- 660//1100
		reloadtime = 2.4,
		weaponvelocity = 380,  -- 300
		areaofeffect = 48,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongaf = "fx",
		explosionart = "explode2",
		startsmoke = 1,
		targetmoveerror = .15,  -- .3
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 180,
			-- subs=0;
		},
	},
}
