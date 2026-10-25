-- CEG definitions (converted from nuketastic.tdf)
-- values are strings on purpose: the CEG parser reads them itself

return {
	london = {
		-- INITIAL SPARK EFFECT
		flamey = {
			class = "heatcloud",
			properties = {
				texture = "burn",
				heat = "40",
				maxheat = "40",
				heatfalloff = "1",
				size = "1",
				sizegrowth = "5",
				speed = "0, 0, 0",
				pos = "0, 5, 0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "2",
		},
		center = {
			class = "heatcloud",
			properties = {
				texture = "burn",
				heat = "25",
				maxheat = "25",
				heatfalloff = "1",
				size = "1",
				sizegrowth = "10",
				speed = "0, 1, 0",
				pos = "r-3 r3, 5, r-3 r3",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "2",
		},
		pikes = {
			class = "explspike",
			properties = {
				dir = "-15 r30,-15 r30,-15 r30",
				width = "150",
				length = "550",
				alpha = "0.99",
				alphadecay = "0.08",
				color = "1.0,1.0,1.0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "20",
		},
		-- THE REAL FX DOWN HERE
		shroom = {
			class = "CExpGenSpawner",
			properties = {
				pos = "0, 0, 0",
				delay = "50",
				explosiongenerator = "custom:ZOE",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
		glow = {
			class = "CExpGenSpawner",
			properties = {
				pos = "0, 0, 0",
				delay = "0 i20",
				explosiongenerator = "custom:LONDON_GLOW",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
		dustring = {
			class = "CExpGenSpawner",
			properties = {
				pos = "0, 0, 0",
				delay = "50",
				explosiongenerator = "custom:LONDON_FLAMES",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
		-- [smolder]
		-- {
		-- class=CExpGenSpawner;
		-- [properties]
		-- {
		-- pos=0, 0, 0;
		-- delay=240 i15;
		-- explosionGenerator=custom:LONDON_SMOLDER;
		-- }
		-- air=1;
		-- water=1;
		-- ground=1;
		-- count=45;
		-- }
		groundflash = {
			flashsize = "3000",
			flashalpha = "3",
			circlegrowth = "6",
			circlealpha = "3",
			ttl = "270",
			color = {1, 0.8, 0.7},
		},
	},
	london_glow = {
		glow = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0",
				sizemod = "1.0",
				pos = "0, 2, 0",
				emitvector = "-0, 1, 0",
				gravity = "0, 0.00, 0",
				colormap = "0 0 0 0.01   1 1 0.8 0.9              0 0 0 0.01",
				texture = "diamondstar",
				airdrag = "1",
				particlelife = "60",
				particlelifespread = "0",
				numparticles = "1",
				particlespeed = "1",
				particlespeedspread = "0",
				particlesize = "1200",
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
		groundflash = {
			flashsize = "1000",
			flashalpha = "1",
			circlegrowth = "0",
			circlealpha = "1",
			ttl = "150",
			color = {1, 0.7, 0.4},
		},
	},
	london_flames = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.0, 0.001 r-0.002",
				colormap = "0 0 0  0.01   0.9 0.9 0 0.5  0.9 0.9 0 0.5  0.9 0.9 0 0.5     0.9 0.9 0 0.5     0.9 0.9 0 0.5       0.8 0.8 0.1 0.5       0.7 0.7 0.2 0.5      0.5 0.35 0. 0.5   0.5 0.35 0. 0.5   0.5 0.35 0. 0.5    0.5 0.35 0. 0.5   0 0 0 0.01",
				texture = "fireball",
				airdrag = "0.97",
				particlelife = "180",
				particlelifespread = "20",
				numparticles = "1",
				particlespeed = "12",
				particlespeedspread = "2",
				particlesize = "40",
				particlesizespread = "20",
				emitrot = "90",
				emitrotspread = "0",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "120",
		},
	},
	london_smolder = {
		smokin = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0 r0.075",
				sizemod = "1.0",
				pos = "0, 4, 0",
				emitvector = "0, 1, 0",
				gravity = "0, 0, 0",
				colormap = "1 1 0.8 0.9      1 0.75 0.5 0.9     1 0.5 0.3 0.9    0.75 0.75 0.5 0.9    0.9 0.9 0.9 0.9    0 0 0 0.01",
				texture = "smokesmall",
				airdrag = "0.995",
				particlelife = "150",
				particlelifespread = "30",
				numparticles = "20",
				particlespeed = "2.5",
				particlespeedspread = "1.25",
				particlesize = "70",
				particlesizespread = "16",
				emitrot = "80",
				emitrotspread = "10",
				directional = "0",
				useairlos = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
	},
	-- ///////////////// ZOE ///////////////////////
	zoe = {
		solange = {
			class = "CExpGenSpawner",
			properties = {
				pos = "0, 0, 0",
				delay = "0 i200",
				explosiongenerator = "custom:SOLANGE",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
		-- [transtheora]
		-- {
		-- class=CExpGenSpawner;
		-- [properties]
		-- {
		-- pos=0, 0, 0;
		-- delay=200 i200;
		-- explosionGenerator=custom:TRANSTHEORA;
		-- }
		-- air=1;
		-- water=1;
		-- ground=1;
		-- count=1;
		-- }
		-- [theora]
		-- {
		-- class=CExpGenSpawner;
		-- [properties]
		-- {
		-- pos=0, 0, 0;
		-- delay=400 i200;
		-- explosionGenerator=custom:THEORA;
		-- }
		-- air=1;
		-- water=1;
		-- ground=1;
		-- count=2;
		-- }
		cap = {
			class = "CExpGenSpawner",
			properties = {
				pos = "-10 r20, 0 i5, -10 r20",
				delay = "0 i4",
				explosiongenerator = "custom:ZOE_CAP",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "50",
		},
		cap2 = {
			class = "CExpGenSpawner",
			properties = {
				pos = "-10 r20, 300 i5, -10 r20",
				delay = "200 i4",
				explosiongenerator = "custom:ZOE_CAP2",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "50",
		},
		cap3 = {
			class = "CExpGenSpawner",
			properties = {
				pos = "-10 r20, 600 i5, -10 r20",
				delay = "400 i4",
				explosiongenerator = "custom:ZOE_CAP3",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "50",
		},
		cap4 = {
			class = "CExpGenSpawner",
			properties = {
				pos = "-10 r20, 863 i5, -10 r20",
				delay = "540 i8",  -- 570 i 8
				explosiongenerator = "custom:ZOE_CAP4",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "25",
		},
		-- [ring]
		-- {
		-- class=CExpGenSpawner;
		-- [properties]
		-- {
		-- pos=-10 r20, 450 i3, -10 r20;
		-- delay=340 i4;
		-- explosionGenerator=custom:ZOE_RING;
		-- }
		-- air=1;
		-- water=1;
		-- ground=1;
		-- count=10;
		-- }
	},
	zoe_cap = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.0, 0.001 r-0.002",
				colormap = "0 0 0  0.01   0.9 0.9 0.9 0.5  0.9 0.9 0.9 0.5  0.9 0.9 0.9 0.5     0.9 0.9 0.9 0.5     0.9 0.9 0.9 0.5       0.8 0.8 0.8 0.5       0.7 0.7 0.7 0.5      0.5 0.5 0.5 0.5   0.5 0.5 0.5 0.5   0.5 0.5 0.5 0.5    0.5 0.5 0.5 0.5   0 0 0 0.01",
				texture = "flame",
				airdrag = "0.96",
				particlelife = "80",
				particlelifespread = "20",
				numparticles = "1",
				particlespeed = "12",
				particlespeedspread = "0",
				particlesize = "60",
				particlesizespread = "60",
				emitrot = "85",
				emitrotspread = "0",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "10",
		},
	},
	zoe_cap2 = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "-0.1",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.05, 0.001 r-0.002",
				colormap = "0 0 0  0.01   0.9 0.9 0 0.5  0.9 0.9 0 0.5  0.9 0.9 0 0.5     0.9 0.9 0 0.5     0.9 0.9 0 0.5       0.8 0.8 0.1 0.5       0.7 0.7 0.2 0.5      0.5 0.35 0. 0.5   0.5 0.35 0. 0.5   0.5 0.35 0. 0.5    0.5 0.35 0. 0.5   0 0 0 0.01",
				texture = "fireball",
				airdrag = "0.97",
				particlelife = "80",
				particlelifespread = "20",
				numparticles = "1",
				particlespeed = "10",
				particlespeedspread = "0",
				particlesize = "70",
				particlesizespread = "70",
				emitrot = "85",
				emitrotspread = "0",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
		socks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.0, 0.001 r-0.002",
				colormap = "0 0 0  0.01   0.9 0.9 0.9 0.5  0.9 0.9 0.9 0.5  0.9 0.9 0.9 0.5     0.9 0.9 0.9 0.5     0.9 0.9 0.9 0.5       0.8 0.8 0.8 0.5       0.7 0.7 0.7 0.5      0.5 0.5 0.5 0.5   0.5 0.5 0.5 0.5   0.5 0.5 0.5 0.5    0.5 0.5 0.5 0.5   0 0 0 0.01",
				texture = "flame",
				airdrag = "0.96",
				particlelife = "80",
				particlelifespread = "20",
				numparticles = "1",
				particlespeed = "10",
				particlespeedspread = "0",
				particlesize = "70",
				particlesizespread = "70",
				emitrot = "85",
				emitrotspread = "0",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
	},
	zoe_cap3 = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "-0.1",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.05, 0.001 r-0.002",
				colormap = "0 0 0  0.01   0.9 0.9 0 0.5  0.9 0.9 0 0.5  0.9 0.9 0 0.5     0.9 0.9 0 0.5     0.9 0.9 0 0.5       0.8 0.8 0.1 0.5       0.7 0.7 0.2 0.5      0.5 0.35 0. 0.5   0.5 0.35 0. 0.5   0.5 0.35 0. 0.5    0.5 0.35 0. 0.5   0 0 0 0.01",
				texture = "fireball",
				airdrag = "0.97",
				particlelife = "60",
				particlelifespread = "40",
				numparticles = "1",
				particlespeed = "8",
				particlespeedspread = "0",
				particlesize = "55",
				particlesizespread = "55",
				emitrot = "85",
				emitrotspread = "0",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "5",
		},
		smoke = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.00, 0.001 r-0.002",
				colormap = "0 0 0  0.01	1 0.7 0.3 0.4	1 0.7 0.3 .5 	1 0.7 0.3 .8 	1 0.7 0.5 1 	1 0.8 0.6 1     1 0.8 0.6 .9     1 0.8 0.6 .9     1 0.8 0.6 .9      0 0 0 0.01",
				texture = "smokesmall",
				airdrag = "0.98",
				particlelife = "90",
				particlelifespread = "40",
				numparticles = "1",
				particlespeed = "8",
				particlespeedspread = "0",
				particlesize = "60",
				particlesizespread = "60",
				emitrot = "85",
				emitrotspread = "0",
				directional = "0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "5",
		},
	},
	zoe_cap4 = {
		smoke = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.00, 0.001 r-0.002",
				colormap = "0 0 0  0.01 1 0.8 0.6 .9     0.8 0.8 0.8 .8        0.8 0.8 0.8 .8  0.6 0.6 0.6 .6  0.4 0.4 0.4 .4  0.2 0.2 0.2 .2  0.1 0.1 0.1 .1  0.05 0.05 0.05 .05  0 0 0 0.01",
				texture = "smokesmall",
				airdrag = "0.98",
				particlelife = "400",
				particlelifespread = "40",
				numparticles = "1",
				particlespeed = "8 i-2.5",
				particlespeedspread = "0",
				particlesize = "120 i12",
				particlesizespread = "20",
				emitrot = "90",
				emitrotspread = "0",
				directional = "0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "3",
		},
	},
	zoe_ring = {
		smoke = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.00, 0.001 r-0.002",
				colormap = "0 0 0  0.01	1 0.7 0.3 0.6	1 0.7 0.5 1 	1 0.7 0.5 1 	1 0.7 0.5 1 	1 0.8 0.6 1     1 0.8 0.6 1     1 0.8 0.6 1     0.8 0.8 0.8 1        0.8 0.8 0.8 1  0.8 0.8 0.8 1  0.8 0.8 0.8 1  0.8 0.8 0.8 1  0.8 0.8 0.8 1  0.8 0.8 0.8 1 0 0 0 0.01",
				texture = "smokesmall",
				airdrag = "0.96",
				particlelife = "790",
				particlelifespread = "40",
				numparticles = "1",
				particlespeed = "24",
				particlespeedspread = "0",
				particlesize = "60",
				particlesizespread = "60",
				emitrot = "85",
				emitrotspread = "0",
				directional = "0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "10",
		},
	},
	-- /////////////// SOLANGE //////////////////////////
	solange = {
		nw = {
			class = "CExpGenSpawner",
			properties = {
				pos = "5 r10, i5, -5 r10",
				delay = "0  i4",
				explosiongenerator = "custom:SOLANGE_PILLAR",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "150",
		},
	},
	solange_pillar = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.01 r-0.02, 0.001 r-0.002",
				colormap = "0 0 0 0.01   0.9 0.9 0 0.5     0.9 0.9 0 0.5       0.8 0.8 0.1 0.5       0.7 0.7 0.2 0.5      0.5 0.35 0. 0.5   0.5 0.35 0. 0.5   0.5 0.35 0. 0.5    0.5 0.35 0. 0.5   0 0 0 0.01",
				texture = "fireball",
				airdrag = "0.97",
				particlelife = "200",
				particlelifespread = "200",
				numparticles = "1",
				particlespeed = "1.5",
				particlespeedspread = "1.5",
				particlesize = "50",
				particlesizespread = "50",
				emitrot = "90",
				emitrotspread = "10",
				directional = "1",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
	},
	-- ////////////////// THEORA /////////////////////
	theora = {
		nw = {
			class = "CExpGenSpawner",
			properties = {
				pos = "5 r10, i5, -5 r10",
				delay = "0  i5",
				explosiongenerator = "custom:THEORA_PILLAR",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "100",
		},
	},
	theora_pillar = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.01 r-0.02, 0.001 r-0.002",
				colormap = "0 0 0  0.01   0.8 0.8 0.8 1       0.8 0.8 0.8 1      0.8 0.8 0.8 1       0.8 0.8 0.8 1      0.8 0.8 0.8 1      0.8 0.8 0.8 1       0 0 0 0.01",
				texture = "smokesmall",
				airdrag = "0.97",
				particlelife = "100",
				particlelifespread = "100",
				numparticles = "1",
				particlespeed = "3",
				particlespeedspread = "3",
				particlesize = "45",
				particlesizespread = "45",
				emitrot = "120",
				emitrotspread = "10",
				directional = "0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
	},
	transtheora = {
		nw = {
			class = "CExpGenSpawner",
			properties = {
				pos = "5 r10, i5, -5 r10",
				delay = "0  i5",
				explosiongenerator = "custom:TRANSTHEORA_PILLAR",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "100",
		},
	},
	transtheora_pillar = {
		rocks = {
			class = "CSimpleParticleSystem",
			properties = {
				sizegrowth = "0.05",
				sizemod = "1.0",
				pos = "0, 0, 0",
				emitvector = "0, 1, 0",
				gravity = "0.001 r-0.002, 0.01 r-0.02, 0.001 r-0.002",
				colormap = "0 0 0  0.01     1 0.6 0 1 	1 0.7 0.3 1 	1 0.7 0.5 1 	1 0.8 0.6 1     0.8 0.8 0.8 1       0 0 0 0.01",
				texture = "smokesmall",
				airdrag = "0.97",
				particlelife = "100",
				particlelifespread = "100",
				numparticles = "1",
				particlespeed = "3",
				particlespeedspread = "3",
				particlesize = "25",
				particlesizespread = "25",
				emitrot = "90",
				emitrotspread = "10",
				directional = "0",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
	},
	offsetlondon = {
		basegoboom_hurray = {
			class = "CExpGenSpawner",
			properties = {
				pos = "-0, -100, 0",
				delay = "0",
				explosiongenerator = "custom:LONDON",
			},
			air = "1",
			water = "1",
			ground = "1",
			count = "1",
		},
	},
}
