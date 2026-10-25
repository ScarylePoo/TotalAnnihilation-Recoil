-- CEG definitions (converted from fusionfx.tdf)
-- values are strings on purpose: the CEG parser reads them itself

return {
	fusionfx = {
		pop1 = {
			class = "heatcloud",
			properties = {
				texture = "blueexplo",  -- bluenovaexplo
				heat = "10",
				maxheat = "10",
				heatfalloff = "0.8",
				size = "0.5",
				sizegrowth = "8",
				pos = "r-2 r2, 5, r-2 r2",
				speed = "0, 0, 0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
		pop2 = {
			class = "heatcloud",
			properties = {
				texture = "blueexplo",  -- brightblueexplo
				heat = "10",
				maxheat = "15",
				heatfalloff = "1",
				size = "0.5",
				sizegrowth = "6",
				pos = "r-3 r3, 5, r-3 r3",
				speed = "0, 1, 0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
	},
	warpexplosion = {
		pikes = {
			class = "explspike",
			properties = {
				dir = "-15 r30,-15 r30,-15 r30",
				width = "50",
				length = "150",
				alpha = "0.99",
				alphadecay = "0.02",
				color = ".4 .7 0.9",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "20",
		},
		glow = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0",
				sizemod = "1.0",
				pos = "0, 2, 0",
				emitvector = "-0, 1, 0",
				gravity = "0, 0.00, 0",
				colormap = "0 0 0 0.01   .4 .7 1 0.9      0 0 0 0.01",
				texture = "diamondstar",
				airdrag = "1",
				particlelife = "15",
				particlelifespread = "0",
				numparticles = "1",
				particlespeed = "1",
				particlespeedspread = "0",
				particlesize = "300",
				particlesizespread = "10",
				emitrot = "0",
				emitrotspread = "180",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
		usedefaultexplosions = "0",
		groundflash = {
			flashsize = "600",  -- flash size
			flashalpha = "1",  -- initial alpha of the flash
			circlegrowth = "15",  -- size increase/frame
			circlealpha = "2",  -- initial alpha of the ring
			ttl = "50",  -- number of frames
			color = {0.2, 0.7, 1},
		},
		water = "1",
		ground = "1",
	},
}
