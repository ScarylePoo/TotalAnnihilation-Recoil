-- CEG definitions (converted from BOTA_Aircraft_Bomb_explosions.tdf)
-- values are strings on purpose: the CEG parser reads them itself

return {
	armbomb_expl = {  -- Blue explosions for ARM - Quanto
		usedefaultexplosions = "1",
		groundflash = {
			texture = "groundring",
			flashsize = "70",  -- 270
			flashalpha = "2",
			circlegrowth = "12",
			circlealpha = ".3",
			ttl = "13",  -- 16
			color = {0.4, 0.2, 1},
		},
		pop1 = {
			class = "heatcloud",
			properties = {
				texture = "2explo",  -- bluenovaexplo
				heat = "10",
				maxheat = "10",
				heatfalloff = "0.8",
				size = "0.5",
				sizegrowth = "5",
				pos = "r-2 r2, 5, r-2 r2",
				speed = "0, 0, 0",
			},
		},
		pikes = {
			class = "explspike",
			properties = {
				dir = "-15 r30,-15 r30,-15 r30",
				width = "50",
				length = "150",
				alpha = "0.99",
				alphadecay = "0.05",
				color = ".4 .7 0.9",
			},
		},
		glow = {
			class = "heatcloud",
			properties = {
				texture = "sparkexplogs",
				heat = "12",
				maxheat = "12",
				heatfalloff = "5",
				size = "10",
				sizegrowth = "30",
				speed = "0, 0, 0",
				pos = "0, 5, 0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
		air = "1",
		water = "1",
		ground = "1",
		count = "1",
	},
	corbomb_expl = {  -- Green explosions for COR
		usedefaultexplosions = "1",
		groundflash = {
			texture = "groundring",
			flashsize = "70",  -- 270
			flashalpha = "2",
			circlegrowth = "12",
			circlealpha = ".3",
			ttl = "13",  -- 16
			color = {0.5, 1, 0.1},
		},
		pop1 = {
			class = "heatcloud",
			properties = {
				texture = "3explo",  -- green explosion
				heat = "10",
				maxheat = "10",
				heatfalloff = "0.8",
				size = "0.5",
				sizegrowth = "5",
				pos = "r-2 r2, 5, r-2 r2",
				speed = "0, 0, 0",
			},
		},
		pikes = {
			class = "explspike",
			properties = {
				dir = "-15 r30,-15 r30,-15 r30",
				width = "50",
				length = "150",
				alpha = "0.99",
				alphadecay = "0.05",
				color = ".4 1 0.1",
			},
		},
		glow = {
			class = "heatcloud",
			properties = {
				texture = "sparkexplogs",
				heat = "12",
				maxheat = "12",
				heatfalloff = "5",
				size = "10",
				sizegrowth = "30",
				speed = "0, 0, 0",
				pos = "0, 5, 0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
		air = "1",
		water = "1",
		ground = "1",
		count = "1",
	},
}
