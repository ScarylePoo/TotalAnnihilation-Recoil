-- genericunitexplosion (all colors)
-- Programmatically generated: edit the tables below, not the output.

-- Per-color values. Add/remove a color here and the loop at the bottom
-- emits the full small/medium/large/huge set for it automatically.
local colors = {
  green = {
    wavemap   = [[0 1 0 0.05  0 0 0 0.0]],
    groundRGB = { 0, 1, 0 },
    poofsmap  = [[1.0 1.0 1.0 0.04  0.5 1.0 0.5 0.01  0.1 0.1 0.1 0.01]],
  },
  orange = {
    wavemap   = [[1 0.5 0 0.05  0 0 0 0.0]],
    groundRGB = { 1, 0.5, 0 },
    poofsmap  = [[1.0 1.0 1.0 0.04  1.0 0.5 0.0 0.01  0.1 0.1 0.1 0.01]],
  },
  purple = {
    wavemap   = [[0.10999999940395 0 0.28999999165535 0.05  0 0 0 0.0]],
    groundRGB = { 0.50999999940395, 0, 0.68999999165535 },
    poofsmap  = [[1.0 1.0 1.0 0.04  0.11 0 0.29 0.01  0.1 0.1 0.1 0.01]],
  },
  red = {
    wavemap   = [[1 0 0 0.05  0 0 0 0.0]],
    groundRGB = { 1, 0, 0 },
    poofsmap  = [[1.0 1.0 1.0 0.04  1.0 0.5 0.5 0.01  0.1 0.1 0.1 0.01]],
  },
  white = {
    wavemap   = [[1 1 1 0.05  0 0 0 0.0]],
    groundRGB = { 1, 1, 1 },
    poofsmap  = [[1.0 1.0 1.0 0.04  1.0 1.0 1.0 0.01  0.1 0.1 0.1 0.01]],
  },
  blue = {
    wavemap   = [[0 0 1 0.05  0 0 0 0.0]],
    groundRGB = { 0, 0, 1 },
    poofsmap  = [[1.0 1.0 1.0 0.04  0.5 0.5 1.0 0.01  0.1 0.1 0.1 0.01]],
  },
}

-- Per-size scaling values. Everything that changes between small/medium/large/huge lives here.
-- TA:Recoil: resized to TA's units (Splinter Faction's values in the comments). Target: the fireball ends at about
-- the size of the unit (radius ~25 / 40 / 65 / 100 elmos: Peewee / Bulldog / Goliath / Krogoth), ring and wave
-- ~1.5x that, ground glow ~1.4x (it lingers). SF's sizes, with their fixed growth over 30-100 frames, reached 65-165 (fireball)
-- and 150-400 (ring) and lit the ground out to 200-800.
local sizes = {
  small = {
    centerSizegrowth    = 2.5,  -- 5
    circlegrowth        = 0.4,  -- 1.5 (x 100 frames)
    waveSize            = 3,    -- 8
    waveSpeed           = 2,    -- 8
    flashsize           = 35,   -- 200
    outerSizegrowth     = 5,    -- 10
    spikeSpeed          = 5,    -- 12
    sparkSize           = 5,    -- 20
    sparkSpeed          = 12,   -- 48
    dirtParticles       = 6,    -- 8
    dirtSize            = 3,    -- 6
    dirtSizeSpread      = 1.5,  -- 3
    dirtSpeed           = 2.5,  -- 5
    dirtSpeedSpread     = 1.5,  -- 3
    dirtSizegrowth      = 0.6,  -- 1.5
    fireballSize        = 12,   -- 20
    fireballGrowth      = 0.4,  -- 1.5 (x 30 frames)
    flareLength         = 15,   -- 40
  },
  medium = {
    centerSizegrowth    = 4,    -- 8
    circlegrowth        = 0.6,  -- 2
    waveSize            = 4,
    waveSpeed           = 2.5,
    flashsize           = 55,   -- 400
    outerSizegrowth     = 7.5,  -- 15
    spikeSpeed          = 7,    -- 16
    sparkSize           = 7,
    sparkSpeed          = 18,
    dirtParticles       = 8,    -- 10
    dirtSize            = 4,    -- 8
    dirtSizeSpread      = 2,    -- 4
    dirtSpeed           = 3.5,  -- 7
    dirtSpeedSpread     = 1.5,  -- 3
    dirtSizegrowth      = 0.8,  -- 1.5
    fireballSize        = 20,   -- 40
    fireballGrowth      = 0.6,
    flareLength         = 24,
  },
  large = {
    centerSizegrowth    = 6,    -- 12
    circlegrowth        = 1.0,  -- 3
    waveSize            = 6,
    waveSpeed           = 3,
    flashsize           = 90,  -- 600
    outerSizegrowth     = 15,   -- 30
    spikeSpeed          = 10,   -- 20
    sparkSize           = 11,
    sparkSpeed          = 28,
    dirtParticles       = 10,   -- 12
    dirtSize            = 5,    -- 10
    dirtSizeSpread      = 2.5,  -- 5
    dirtSpeed           = 5,    -- 10
    dirtSpeedSpread     = 2,    -- 4
    dirtSizegrowth      = 1.0,  -- 1.5
    fireballSize        = 32,   -- 80
    fireballGrowth      = 1.0,
    flareLength         = 38,
  },
  huge = {
    centerSizegrowth    = 9,    -- 18
    circlegrowth        = 1.5,  -- 4
    waveSize            = 8,
    waveSpeed           = 4,
    flashsize           = 140,  -- 800
    outerSizegrowth     = 20,   -- 40
    spikeSpeed          = 14,   -- 26
    sparkSize           = 16,
    sparkSpeed          = 40,
    dirtParticles       = 12,   -- 14
    dirtSize            = 7,    -- 12
    dirtSizeSpread      = 3,    -- 6
    dirtSpeed           = 7,    -- 14
    dirtSpeedSpread     = 2,    -- 4
    dirtSizegrowth      = 1.2,  -- 1.5
    fireballSize        = 50,   -- 120
    fireballGrowth      = 1.6,
    flareLength         = 60,
  },
}

-- s = size params, c = color params
local function makeExplosion(s, c)
  return {
    centerflare = {
      air        = true,
      class      = [[heatcloud]],
      count      = 1,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        alwaysvisible = true,
        heat          = 10,
        heatfalloff   = 1.3,
        maxheat       = 20,
        pos           = [[r-2 r2, 5, r-2 r2]],
        size          = 1,
        sizegrowth    = s.centerSizegrowth,
        speed         = [[0, 1 0, 0]],
        texture       = [[flare]],
      },
    },

    -- put this next to groundflash
    explosionwave = {
      air        = true,
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      ground     = false,
      water      = true,
      underwater = true,
      properties = {
        airdrag             = 0.87,
        alwaysvisible       = true,
        colormap            = c.wavemap, -- same as groundflash colors
        directional         = false,
        emitrot             = 90,
        emitrotspread       = 5,
        emitvector          = [[0, 0, 0]],
        gravity             = [[0, 0, 0]],
        numparticles        = 1,
        particlelife        = 100, -- same as groundflash ttl
        particlelifespread  = 0,
        particlesize        = s.waveSize,
        particlesizespread  = 1,
        particlespeed       = s.waveSpeed,
        particlespeedspread = s.waveSpeed * 0.75,
        pos                 = [[0, 1, 0]],
        sizegrowth          = s.circlegrowth, -- same as groundflash circlegrowth
        sizemod             = 1.0,
        texture             = [[explosionwave]],
      },
    },

    groundflash = {
      air           = true,
      alwaysvisible = true,
      circlealpha   = 0.6,
      circlegrowth  = s.circlegrowth,
      flashalpha    = 0.6,
      flashsize     = s.flashsize,
      ground        = true,
      ttl           = 100,
      water         = true,
      underwater    = true,
      color = {
        [1] = c.groundRGB[1],
        [2] = c.groundRGB[2],
        [3] = c.groundRGB[3],
      },
    },

    kickedupdirt = {
      air        = true,
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      ground     = true,
      properties = {
        airdrag             = 0.87,
        alwaysvisible       = true,
        colormap            = [[0.25 0.20 0.10 0.35  0 0 0 0.0]],
        directional         = false,
        emitrot             = 90,
        emitrotspread       = 20,
        emitvector          = [[0, 1, 0]],
        gravity             = [[0, -0.05, 0]],
        numparticles        = s.dirtParticles,
        particlelife        = 5,
        particlelifespread  = 15,
        particlesize        = s.dirtSize,
        particlesizespread  = s.dirtSizeSpread,
        particlespeed       = s.dirtSpeed,
        particlespeedspread = s.dirtSpeedSpread,
        pos                 = [[0, 1, 0]],
        sizegrowth          = s.dirtSizegrowth,
        sizemod             = 1.0,
        texture             = [[bigexplosmoke]],
      },
    },

    kickedupwater = {
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      water      = true,
      underwater = true,
      properties = {
        airdrag             = 0.87,
        alwaysvisible       = true,
        colormap            = [[0.7 0.7 0.9 0.35  0 0 0 0.0]],
        directional         = false,
        emitrot             = 90,
        emitrotspread       = 20,
        emitvector          = [[0, 1, 0]],
        gravity             = [[0, -0.05, 0]],
        numparticles        = s.dirtParticles,
        particlelife        = 5,
        particlelifespread  = 15,
        particlesize        = s.dirtSize,
        particlesizespread  = s.dirtSizeSpread,
        particlespeed       = s.dirtSpeed,
        particlespeedspread = s.dirtSpeedSpread,
        pos                 = [[0, 1, 0]],
        sizegrowth          = s.dirtSizegrowth,
        sizemod             = 1.0,
        texture             = [[wake]],
      },
    },

    orangeexplosionspikes = {
      air        = true,
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        airdrag             = 0.8,
        alwaysvisible       = true,
        colormap            = [[0.7 0.8 0.9 0.03   0.9 0.5 0.2 0.01]],
        directional         = true,
        emitrot             = 45,
        emitrotspread       = 32,
        emitvector          = [[0, 1, 0]],
        gravity             = [[0, -0.01, 0]],
        numparticles        = 8,
        particlelife        = 8,
        particlelifespread  = 0,
        particlesize        = 1,
        particlesizespread  = 0,
        particlespeed       = s.spikeSpeed,
        particlespeedspread = 2,
        pos                 = [[0, 2, 0]],
        sizegrowth          = 1,
        sizemod             = 1,
        texture             = [[flashside2]],
        useairlos           = false,
      },
    },

    outerflash = {
      air        = true,
      class      = [[heatcloud]],
      count      = 2,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        alwaysvisible = true,
        heat          = 10,
        heatfalloff   = 1.1,
        maxheat       = 20,
        pos           = [[r-2 r2, 5, r-2 r2]],
        size          = 1,
        sizegrowth    = s.outerSizegrowth,
        speed         = [[0, 1 0, 0]],
        texture       = [[brightblueexplo]],
      },
    },

    unitpoofs = {
      air        = true,
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        airdrag             = 0.2,
        alwaysvisible       = true,
        colormap            = c.poofsmap,
        directional         = false,
        emitrot             = 45,
        emitrotspread       = 32,
        emitvector          = [[0, 1, 0]],
        gravity             = [[0, 0.05, 0]],
        numparticles        = 8,
        particlelife        = 5,
        particlelifespread  = 16,
        particlesize        = s.sparkSize,
        particlesizespread  = 0,
        particlespeed       = s.sparkSpeed,
        particlespeedspread = 1,
        pos                 = [[0, 2, 0]],
        sizegrowth          = 0.8,
        sizemod             = 1,
        texture             = [[randomdots]],
        useairlos           = false,
      },
    },

    fireball = {
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      air        = true,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        airdrag             = 0.97,
        colormap            = [[1 1 1 0.1   1 1 1 0.1   1 1 1 0.1   1 1 1 0.1   0 0 0 0]],
        directional         = false,
        emitrot             = 0,
        emitrotspread       = 0,
        emitvector          = [[0,0,0]],
        gravity             = [[0,0.1,0]],
        numparticles        = 1,
        particlelife        = 30,
        particlelifespread  = 9,
        particlesize        = s.fireballSize,
        particlesizespread  = 0,
        particlespeed       = 0,
        particlespeedspread = 0,
        rotParams           = [[-24 r48, -60 r120, -180 r360]],
        animParams          = [[6,6,40]], --[xTiles, yTiles, animLength in game frames]
        pos                 = [[0,0,0]],
        sizegrowth          = s.fireballGrowth,
        sizemod             = 1,
        texture             = [[generated-unitexplosion-static]],
        drawOrder           = 0,
        -- castshadow          = true,
      },
    },

    brightflare = {
      air                = true,
      class              = [[CBitmapMuzzleFlame]],
      count              = 1,
      ground             = true,
      underwater         = true,
      water              = true,
      properties = {
        colormap            = [[1 1 1 0.1   1 1 1 0.1   1 1 1 0.1   1 1 1 0.1   0 0 0 0]],
        dir                = [[0, 1, 0]],
        --gravity            = [[0.0, 0.1, 0.0]],
        frontoffset        = 0,
        animParams1          = [[6,6,40]],  -- front texture (engine 2026.09: muzzle flames read animParams1/2, not animParams)
        animParams2          = [[6,6,40]],  -- side texture --[xTiles, yTiles, animLength in game frames]
        fronttexture       = [[generated-furnace]],
        length             = s.flareLength,
        sidetexture        = [[none]],
        size               = s.fireballSize,
        sizegrowth         = 0,
        ttl                = 30,
        pos                = [[0, 3, 0]],
        --rotParams          = [[-10 r20, -20 r40, -180 r360]],
        drawOrder          = 0,
      },
    },
  }
end

-- Build and return the final table.
-- Keys stay identical to the old per-color files: genericunitexplosion-<size>-<color>
local result = {}
for colorName, c in pairs(colors) do
  for sizeName, s in pairs(sizes) do
    result["genericunitexplosion-" .. sizeName .. "-" .. colorName] = makeExplosion(s, c)
  end
end
return result
