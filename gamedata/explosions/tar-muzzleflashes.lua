-- TA:Recoil muzzle flashes, sized per weapon (gamedata/alldefs_post.lua MuzzleCEG picks one; spawned by
-- luarules/gadgets/fx_muzzle.lua when the weapon fires).
--
--   tar-muzzle-cannon-<size>          Splinter Faction's "gdhcannon" (unit muzzle flash.lua): a flame cone with a
--                                      front flare, plus an ejected shell casing (not on the tiny one)
--   tar-muzzle-energy-<size>-<colour> Splinter Faction's "electricity": two flickering light balls and an expanding
--                                      ring, the ring in the laser's colour
--
-- size: tiny (E.M.G.s, light lasers) < small < medium < large < huge (Big Bertha, Annihilators)

local SIZES = {
	--            cannon flame              casing           energy ball  ring growth  life (frames)
	tiny   = { size = 3,  length = 10,  casing = 0,   ball = 5,  ring = 0.35, life = 10 },
	small  = { size = 5,  length = 17,  casing = 2,   ball = 8,  ring = 0.55, life = 12 },
	medium = { size = 9,  length = 30,  casing = 3,   ball = 12, ring = 0.8,  life = 15 },
	large  = { size = 14, length = 46,  casing = 4,   ball = 18, ring = 1.2,  life = 18 },
	huge   = { size = 22, length = 75,  casing = 6,   ball = 28, ring = 2.0,  life = 22 },
}

local RING = {
	red    = { 1.0, 0.1, 0.05 },
	green  = { 0.2, 1.0, 0.2 },
	blue   = { 0.25, 0.5, 1.0 },
	purple = { 0.8, 0.25, 1.0 },
	orange = { 1.0, 0.55, 0.1 },
	white  = { 0.9, 0.9, 1.0 },
}

local function cannon(s)
	local t = {
		usedefaultexplosions = false,
		flame = {
			air = true, ground = true, water = true, underwater = 1, count = 1,
			class = [[CBitmapMuzzleFlame]],
			properties = {
				colormap     = [[1 0.7 0.4 0.01 1 0.2 0.1 0.01 0 0 0 0.01]],
				dir          = [[dir]],
				frontoffset  = 0,
				fronttexture = [[shotgunflare]],
				sidetexture  = [[shotgunside]],
				length       = s.length,
				size         = s.size,
				sizegrowth   = -1,
				ttl          = 15,
			},
		},
	}
	if s.casing > 0 then
		t.shells = {
			air = true, ground = true, water = true, count = 1,
			class = [[CSimpleParticleSystem]],
			properties = {
				airdrag             = 0.97,
				colormap            = [[1 1 1 1   1 1 1 1]],
				directional         = true,
				emitrot             = 180,
				emitrotspread       = 10,
				emitvector          = [[dir]],
				gravity             = [[0, -0.1, 0]],
				numparticles        = 1,
				particlelife        = 30,
				particlelifespread  = 30,
				particlesize        = s.casing,
				particlesizespread  = 0,
				particlespeed       = 2 + s.casing * 0.5,
				particlespeedspread = 0,
				pos                 = [[0, 0, 0]],
				rotParams           = [[-24 r48, -60 r120, -180 r360]],
				sizegrowth          = 0,
				sizemod             = 1.0,
				texture             = [[silvershell]],
			},
		}
	end
	return t
end

local function ball(s, texture, colormap)
	return {
		air = true, ground = true, water = true, count = 1,
		class = [[CSimpleParticleSystem]],
		properties = {
			airdrag             = 0.95,
			colormap            = colormap,
			directional         = false,
			emitrot             = 0,
			emitrotspread       = 1,
			emitvector          = [[dir]],
			gravity             = [[0, 0, 0]],
			numparticles        = 1,
			particlelife        = s.life,
			particlelifespread  = 0,
			particlesize        = s.ball,
			particlesizespread  = 0,
			particlespeed       = 0,
			particlespeedspread = 0,
			pos                 = [[0, 0, 0]],
			sizegrowth          = 0,
			sizemod             = 1.0,
			texture             = texture,
		},
	}
end

local function energy(s, c)
	local r, g, b = c[1], c[2], c[3]
	local ring = ball(s, [[lightring]], string.format("%.2f %.2f %.2f 0.01  %.2f %.2f %.2f 0.01  0 0 0 0.01",
		r, g, b, r * 0.7, g * 0.7, b * 0.7))
	ring.properties.particlesize = math.max(1, s.ball / 15)
	ring.properties.sizegrowth = s.ring
	return {
		usedefaultexplosions = false,
		-- the first ball takes the weapon's colour (lightened), so a red laser flashes red; the second stays white-hot
		lightball50 = ball(s, [[lightb3]], string.format("%.2f %.2f %.2f 0.01  %.2f %.2f %.2f 0.01  0 0 0 0.01",
			0.2 + r * 0.6, 0.2 + g * 0.6, 0.2 + b * 0.6, 0.3 + r * 0.7, 0.3 + g * 0.7, 0.3 + b * 0.7)),
		lightball52 = ball(s, [[lightb4]], [[0 0 0 0.01 0 0 0 0.01 0.7 0.7 0.7 0.01  1 1 1 0.01  0 0 0 0.01]]),
		lightring50 = ring,
	}
end

local defs = {}
for name, s in pairs(SIZES) do
	defs["tar-muzzle-cannon-" .. name] = cannon(s)
	for colour, c in pairs(RING) do
		defs["tar-muzzle-energy-" .. name .. "-" .. colour] = energy(s, c)
	end
end
return defs
