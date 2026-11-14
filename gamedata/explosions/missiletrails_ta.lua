-- TA:Recoil missile trails: missiletrail-ta-<size>[-<colour>], given to every MissileLauncher and StarburstLauncher
-- by WeaponDef_Post (gamedata/alldefs_post.lua, MissileTrail). The engine spawns the CEG every frame at the
-- projectile's origin, which is the missile's tail (tools/s3okit/kit/make_missiles.py), so it all comes out of the
-- nozzle. The engine's own smoke ribbon (smoketrail = 1) stays as the long-lived part.
--
-- Everything here is short-lived and additive (colormap alpha near 0): it reads as light, not as smoke, so a missile
-- salvo sparkles without leaving a curtain over the battlefield.
--   flame   a hot jet pointing back along the flight direction, flickering in length
--   glow    a bright bloom on the nozzle
--   sparks  streaks thrown back out of the jet, falling and cooling as they go
--   embers  a few slow glittering motes left hanging in the air for half a second
--   ring    (strategic missiles) a faint shock ring now and then, a heavy-motor shimmer

local SIZES = {
	--               scale  sparks per frame   embers per frame  ring
	small     = { s = 0.75, sparks = "0.5 r1",   embers = "0 r1.2", ring = false },
	medium    = { s = 1.15, sparks = "0.8 r1.4", embers = "0 r1.5", ring = false },
	large     = { s = 1.6,  sparks = "1 r2",     embers = "0.3 r1.5", ring = false },
	strategic = { s = 2.4,  sparks = "2 r2",     embers = "1 r2",   ring = true },
}

-- hot core, flame body, cooling tail (rgb)
local PALETTES = {
	[""]       = { hot = { 1.0, 0.96, 0.82 }, mid = { 1.0, 0.58, 0.16 }, cool = { 0.75, 0.18, 0.03 } },
	["-emp"]   = { hot = { 0.92, 0.96, 1.0 }, mid = { 0.38, 0.62, 1.0 },  cool = { 0.16, 0.22, 0.85 } },
	["-green"] = { hot = { 0.94, 1.0, 0.9 },  mid = { 0.5, 1.0, 0.42 },   cool = { 0.1, 0.55, 0.12 } },
}

local function c(rgb, k, a)
	return string.format("%.3f %.3f %.3f %.3f", rgb[1] * k, rgb[2] * k, rgb[3] * k, a)
end

local function f(x)
	return string.format("%.2f", x)
end

local function trail(size, pal)
	local s = size.s
	local t = {
		flame = {
			air = true, ground = true, water = true, underwater = false,
			class = [[CBitmapMuzzleFlame]],
			count = 1,
			properties = {
				colormap = table.concat({ c(pal.hot, 1, 0.01), c(pal.mid, 0.9, 0.008), c(pal.cool, 0.6, 0.005), "0 0 0 0.01" }, "   "),
				dir = [[dir]],
				frontoffset = 0,
				fronttexture = [[none]],
				length = "-" .. f(10 * s) .. " r" .. f(4 * s),   -- negative: behind the nozzle
				sidetexture = [[muzzleside]],
				size = f(1.9 * s) .. " r" .. f(0.6 * s),
				sizegrowth = -0.15,
				ttl = 2,
				useairlos = true,
			},
		},
		glow = {
			air = true, ground = true, water = true, underwater = false,
			class = [[CSimpleParticleSystem]],
			count = 1,
			properties = {
				airdrag = 1,
				colormap = table.concat({ c(pal.hot, 0.55, 0.0), c(pal.mid, 0.3, 0.0), "0 0 0 0.01" }, "   "),
				directional = false,
				emitrot = 0, emitrotspread = 0, emitvector = [[dir]],
				gravity = [[0, 0, 0]],
				numparticles = 1,
				particlelife = 2, particlelifespread = 1,
				particlesize = f(4.5 * s), particlesizespread = f(2 * s),
				particlespeed = 0, particlespeedspread = 0,
				pos = [[0, 0, 0]],
				sizegrowth = 0, sizemod = 1,
				texture = [[flare]],
				useairlos = true,
			},
		},
		sparks = {
			air = true, ground = true, water = true, underwater = false,
			class = [[CSimpleParticleSystem]],
			count = 1,
			properties = {
				airdrag = 0.9,
				colormap = table.concat({ c(pal.hot, 1, 0.01), c(pal.mid, 1, 0.01), c(pal.cool, 0.8, 0.005), "0 0 0 0.01" }, "   "),
				directional = true,
				emitrot = 0, emitrotspread = 22, emitvector = [[dir]],
				gravity = [[0, -0.09, 0]],
				numparticles = size.sparks,
				particlelife = 6, particlelifespread = 8,
				particlesize = f(1.5 * s), particlesizespread = f(0.8 * s),
				particlespeed = f(-6 * s - 2), particlespeedspread = f(3 * s),     -- thrown back out of the jet
				pos = [[0, 0, 0]],
				sizegrowth = 0, sizemod = 0.93,
				texture = [[gunshot]],
				useairlos = true,
			},
		},
		embers = {
			air = true, ground = true, water = true, underwater = false,
			class = [[CSimpleParticleSystem]],
			count = 1,
			properties = {
				airdrag = 0.88,
				colormap = table.concat({ c(pal.hot, 0.9, 0.01), c(pal.mid, 0.8, 0.01), c(pal.cool, 0.6, 0.005), "0 0 0 0.01" }, "   "),
				directional = false,
				emitrot = 0, emitrotspread = 180, emitvector = [[dir]],
				gravity = [[0, 0.025, 0]],                                       -- heat lifts them a little
				numparticles = size.embers,
				particlelife = 14, particlelifespread = 16,
				particlesize = f(0.9 * s), particlesizespread = f(0.6 * s),
				particlespeed = 0.3, particlespeedspread = f(0.8 * s),
				pos = [[0, 0, 0]],
				sizegrowth = 0, sizemod = 0.97,
				texture = [[flare]],
				useairlos = true,
			},
		},
	}
	if size.ring then
		t.ring = {
			air = true, ground = true, water = true, underwater = false,
			class = [[CSimpleParticleSystem]],
			count = 1,
			properties = {
				airdrag = 1,
				colormap = table.concat({ c(pal.mid, 0.35, 0.0), c(pal.cool, 0.15, 0.0), "0 0 0 0.01" }, "   "),
				directional = false,
				emitrot = 0, emitrotspread = 0, emitvector = [[dir]],
				gravity = [[0, 0, 0]],
				numparticles = "0 r1.12",                                         -- about one frame in eight
				particlelife = 9, particlelifespread = 3,
				particlesize = f(3 * s), particlesizespread = 0,
				particlespeed = 0, particlespeedspread = 0,
				pos = [[0, 0, 0]],
				sizegrowth = f(1.1 * s), sizemod = 1,
				texture = [[circularthingy]],
				useairlos = true,
			},
		}
	end
	return t
end

local defs = {}
for sizeName, size in pairs(SIZES) do
	for suffix, pal in pairs(PALETTES) do
		defs["missiletrail-ta-" .. sizeName .. suffix] = trail(size, pal)
	end
end
return defs
