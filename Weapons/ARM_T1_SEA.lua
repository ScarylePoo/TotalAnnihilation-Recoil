-- Weapon definitions (converted from ARM_T1_SEA.TDF)

return {
	arm_roy = {
		id = 64,
		name = "Heavy Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -25,
		range = 950,  -- 660//1155
		reloadtime = 2,
		weaponvelocity = 380,  -- 300
		areaofeffect = 48,
		soundstart = "cannon3",
		soundhit = "xplomed2",
		accuracy = 300,
		startsmoke = 1,
		targetmoveerror = .15,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 165,
		},
	},
}
