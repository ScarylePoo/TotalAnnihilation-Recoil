-- Game rules (converted from Modrules.TDF)

return {
	featurelos = {
		featurevisibility = 2,
	},
	flankingbonus = {
		defaultmode = 0,  -- defaults to 1
	},
	reclaim = {
		reclaimmethod = 0,
	},
	sensors = {
		los = {
			losmiplevel = 3,
			airmiplevel = 4,  -- was airlosmiplevel, a key Recoil does not read (it read the default, 1); losmul/airlosmul are not read either
		},
	},
}
