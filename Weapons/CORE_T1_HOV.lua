-- Weapon definitions (native Recoil tags; converted from CORE_T1_HOV.TDF)

return {
	corsnap_weapon = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 507,  -- 290
		reloadtime = 1.3,
		weaponvelocity = 260,
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannon2",
		soundhit = "xplomed4",
		damage = {
			default = 85,
		},
	},
}
