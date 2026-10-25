-- CEG definitions (converted from torpedoold.tdf)
-- values are strings on purpose: the CEG parser reads them itself

return {
	torpedoold = {
		usedefaultexplosions = "0",
		bluesphere = {
			class = "CSpherePartSpawner",
			properties = {
				ttl = "30",
				alpha = "0.33",
				expansionspeed = "0.4 r0.4",
				color = "0.1, 0.4, 1.0",
			},
			ground = "0",
			air = "0",
			count = "1",
			water = "1",
		},
		waterbubble = {
			class = "heatcloud",
			properties = {
				heat = "15",
				texture = "bubble",
				maxheat = "15",
				heatfalloff = "0.2",
				size = "8.00",
				sizegrowth = "-0.2",
				sizemod = "0",
				sizemodmod = "0",
				speed = "-0.75 r1.5, -0.5 r0.4, -0.75 r1.5",
				pos = "1.3 r-2.6, 0.4 r-0.6, 1.3 r-2.6",
			},
			air = "0",
			water = "1",
			underwater = "1",
			ground = "0",
			count = "15",
		},
		watercloud = {
			class = "heatcloud",
			properties = {
				heat = "15",
				texture = "water",
				maxheat = "15",
				heatfalloff = "0.6",
				size = "1.85",
				sizegrowth = "2.9",
				sizemod = "0",
				sizemodmod = "0",
				speed = "-0.4 r0.8, -0.5 r0.4, -0.4 r0.8",
				pos = "0.1 r-0.2, 0.1 r-0.2, 0.1 r-0.2",
			},
			air = "0",
			water = "1",
			underwater = "1",
			ground = "0",
			count = "2",
		},
		spark_sprey = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "-0.02",
				sizemod = "1.0",
				pos = "0, 2, 0",
				gravity = "0, 0, 0",
				colormap = "1 1 1 0.01   0.2 0.7 1.0 0.01   0.1 0.35 0.5 0.01   0.1 0.35 0.5 0.01",
				texture = "splash",
				airdrag = "0.8",
				particlelifespread = "0.1",  -- random decay//
				particlespeedspread = "0.8",  -- random speed//
				particlesizespread = "0.7",  -- random sise//
				particlelife = "55",
				numparticles = "15",
				particlespeed = "1.1",
				particlesize = "7",
				emitvector = "dir",  -- direction of particles//
				emitrot = "165",
				emitrotspread = "15",
				directional = "1",
				useairlos = "1",
			},
			air = "0",
			water = "0",
			underwater = "0",
			ground = "0",
			count = "1",
		},
		windsphere = {
			class = "CSpherePartSpawner",
			properties = {
				ttl = "15",
				alpha = "0.55",
				expansionspeed = "1 r1",
				color = "1.0, 0.6 r0.3, 0.1 r0.8",
			},
			ground = "1",
			air = "1",
			water = "0",
			count = "1",
		},
		heatcloud = {
			properties = {
				heat = "15",
				texture = "firecloud",
				maxheat = "15",
				heatfalloff = "0.86",
				size = "1.45",
				sizegrowth = "1.1",
				sizemod = "0",
				sizemodmod = "0",
				speed = "-0.2 r0.4, -0.2 r0.4, -0.2 r0.4",
				pos = "0.1 r-0.2, 0.1 r-0.2, 0.1 r-0.2",
			},
			air = "1",
			water = "0",
			ground = "1",
			count = "4",
		},
		spikes = {
			class = "explspike",
			properties = {
				dir = "-45 r90,-45 r90,-45 r90",
				width = "1.5",  -- 2.5;
				length = "0.04",  -- 1
				alpha = "0.5",  -- 0.5//
				alphadecay = "0.09",  -- 0.02//
				color = "1, 1, 0",  -- yellow spike//
			},
			air = "1",
			water = "0",
			ground = "1",
			count = "8",
		},
		dirt = {
			properties = {
				color = "1, 1, 1",
				size = "10",
				sizeexpansion = "0.5",
				slowdown = "1",
				-- lifetime=160; -- unknown tag in spring 95
				pos = "-2 r4,-2 r4, -2 r4",
				speed = "0.75 r-1.5, 1.5 r3.0, 0.75 r-1.5",
			},
			water = "1",
			underwater = "0",
			count = "10",
		},
		groundflash = {
			flashsize = "67",
			flashalpha = "0.55",
			circlegrowth = "1",
			circlealpha = "0.55",
			ttl = "20",
			color = {0.7, 0.5, 0},
			air = "1",
			ground = "1",
			water = "0",
		},
	},
}
