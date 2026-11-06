-- Weapon definitions (converted from BOTA_Krogoth.TDF)

return {
	krogoth_arm_cannon = {
		weapontype = "Cannon",  -- was EmgCannon; TA "Gauss Cannon" corkrog_fire as a Cannon (user decision)
		-- used by units
		-- CORE_T3_BOT_Krogoth
		-- type
		turret = 1,
		-- sounds
		soundstart = "Krogun1",
		soundhit = "xplomed2",
		-- behaviour
		tolerance = 500,
		weaponvelocity = 450,  -- TA 3.1c (was 700)
		-- stats
		range = 300,  -- TA 3.1c (was 525)
		reloadtime = 1.6,
		areaofeffect = 8,  -- TA 3.1c (was 48)
		damage = {
			default = 480,
		},
	},
}
