-- Weapon definitions (converted from BOTA_Krogoth.TDF)

return {
	krogoth_arm_cannon = {
		-- used by units
		-- CORE_T3_BOT_Krogoth
		-- type
		weapontype = "EmgCannon",
		turret = 1,
		-- sounds
		soundstart = "Krogun1",
		soundhit = "xplomed2",
		-- behaviour
		tolerance = 500,
		weaponvelocity = 700,
		-- stats
		range = 525,
		reloadtime = 1.6,
		areaofeffect = 48,
		damage = {
			default = 480,
		},
	},
}
