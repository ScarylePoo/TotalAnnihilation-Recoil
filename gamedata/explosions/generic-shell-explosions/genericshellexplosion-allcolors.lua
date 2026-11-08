-- genericshellexplosion (all colors)
-- Programmatically generated: edit the tables below, not the output.

-- Per-color values. Add/remove a color here and the loop at the bottom
-- emits the full small/medium/large set for it automatically.
local colors = {
  green = {
    wavemap   = [[0 1 0 0.05  0 0 0 0.0]],
    groundRGB = { 0, 1, 0 },
    poofsmap  = [[1.0 1.0 1.0 0.04  0.5 1.0 0.5 0.01  0.1 0.1 0.1 0.01]],
    outerTex  = [[greennovaexplo]],
  },
  orange = {
    wavemap   = [[1 0.5 0 0.05  0 0 0 0.0]],
    groundRGB = { 1, 0.5, 0 },
    poofsmap  = [[1.0 1.0 1.0 0.04  1.0 0.5 0.0 0.01  0.1 0.1 0.1 0.01]],
    outerTex  = [[orangenovaexplo]],
  },
  purple = {
    wavemap   = [[0.10999999940395 0 0.28999999165535 0.05  0 0 0 0.0]],
    groundRGB = { 0.50999999940395, 0, 0.68999999165535 },
    poofsmap  = [[1.0 1.0 1.0 0.04  0.11 0 0.29 0.01  0.1 0.1 0.1 0.01]],
    outerTex  = [[purplenovaexplo]],
  },
  red = {
    wavemap   = [[1 0 0 0.05  0 0 0 0.0]],
    groundRGB = { 1, 0, 0 },
    poofsmap  = [[1.0 1.0 1.0 0.04  1.0 0.5 0.5 0.01  0.1 0.1 0.1 0.01]],
    outerTex  = [[rednovaexplo]],
  },
  white = {
    wavemap   = [[1 1 1 0.05  0 0 0 0.0]],
    groundRGB = { 1, 1, 1 },
    poofsmap  = [[1.0 1.0 1.0 0.04  1.0 1.0 1.0 0.01  0.1 0.1 0.1 0.01]],
    outerTex  = [[brightblueexplo]],
  },
  blue = {
    wavemap   = [[0 0 1 0.05  0 0 0 0.0]],
    groundRGB = { 0, 0, 1 },
    poofsmap  = [[1.0 1.0 1.0 0.04  0.5 0.5 1.0 0.01  0.1 0.1 0.1 0.01]],
    outerTex  = [[bluenovaexplo]],
  },
}

-- Per-size scaling values. Everything that changes between small/medium/large lives here.
-- TA:Recoil: half of Splinter Faction's sizes, and the shock wave / ground ring 40 % (SF's were far bigger than
-- TA's units and blast radii: SF's large ring reached ~240 elmos). SF's values in the comments.
local sizes = {
  small = {
    -- centerflare
    centerSizegrowth    = 2.5,  -- 5
    -- explosionwave / groundflash
    circlegrowth        = 1.2,  -- 3
    waveSpeed           = 3,    -- 8 (the wave particle's drift)
    flashsize           = 25,   -- 50
    -- outerflash
    outerSizegrowth     = 5,    -- 10
    -- orangeexplosionspikes
    spikeSpeed          = 4,    -- 8
    -- kickedupdirt / kickedupwater
    dirtParticles       = 5,
    dirtSize            = 2,    -- 4
    dirtSizeSpread      = 1,    -- 2
    dirtSpeed           = 1.5,  -- 3
    dirtSpeedSpread     = 1,    -- 2
    dirtSizegrowth      = 0.5,  -- 1
    -- fireball (shrinks over time, impact flash)
    fireballSize        = 18,   -- 35
    smokeExtra          = 10,   -- 20 (smoke = fireball + this)
    flareExtra          = 15,   -- 30 (bright flare = fireball + this)
    flareLength         = 20,   -- 40
  },
  medium = {
    centerSizegrowth    = 4,    -- 8
    circlegrowth        = 2.4,  -- 6
    waveSpeed           = 3,    -- 8
    flashsize           = 50,   -- 100
    outerSizegrowth     = 7.5,  -- 15
    spikeSpeed          = 8,    -- 16
    dirtParticles       = 7,
    dirtSize            = 2.5,  -- 5
    dirtSizeSpread      = 1.5,  -- 3
    dirtSpeed           = 2.5,  -- 5
    dirtSpeedSpread     = 1,    -- 2
    dirtSizegrowth      = 0.5,  -- 1
    fireballSize        = 30,   -- 60
    smokeExtra          = 10,
    flareExtra          = 15,
    flareLength         = 20,
  },
  large = {
    centerSizegrowth    = 6,    -- 12
    circlegrowth        = 4.8,  -- 12
    waveSpeed           = 3,    -- 8
    flashsize           = 75,   -- 150
    outerSizegrowth     = 15,   -- 30
    spikeSpeed          = 12,   -- 24
    dirtParticles       = 10,
    dirtSize            = 3,    -- 6
    dirtSizeSpread      = 1.5,  -- 3
    dirtSpeed           = 3.5,  -- 7
    dirtSpeedSpread     = 1.5,  -- 3
    dirtSizegrowth      = 0.5,  -- 1
    fireballSize        = 40,   -- 80
    smokeExtra          = 10,
    flareExtra          = 15,
    flareLength         = 20,
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
        particlelife        = 20, -- same as groundflash ttl
        particlelifespread  = 0,
        particlesize        = s.circlegrowth / 3,
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
      flashalpha    = 0.9,
      flashsize     = s.flashsize,
      ground        = true,
      ttl           = 20,
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
        particlelifespread  = 10,
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
        particlelifespread  = 10,
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
        sizegrowth          = 0.5,
        sizemod             = 1,
        texture             = [[flashside2]],
        useairlos           = false,
      },
    },

    --outerflash = {
    --  air        = true,
    --  class      = [[heatcloud]],
    --  count      = 2,
    --  ground     = true,
    --  water      = true,
    --  underwater = true,
    --  properties = {
    --    alwaysvisible = true,
    --    heat          = 10,
    --    heatfalloff   = 1.1,
    --    maxheat       = 20,
    --    pos           = [[r-2 r2, 5, r-2 r2]],
    --    size          = 1,
    --    sizegrowth    = s.outerSizegrowth,
    --    speed         = [[0, 1 0, 0]],
    --    texture       = c.outerTex,
    --  },
    --},

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
        gravity             = [[0,0,0]],
        numparticles        = 1,
        particlelife        = 15,
        particlelifespread  = 9,
        particlesize        = s.fireballSize,
        particlesizespread  = 0,
        particlespeed       = 0,
        particlespeedspread = 0,
        rotParams           = [[-24 r48, -60 r120, -180 r360]],
        animParams          = [[7,7,30]], --[xTiles, yTiles, animLength in game frames]
        pos                 = [[0,0,0]],
        sizegrowth          = -0.5,
        sizemod             = 1,
        texture             = [[generated-impact3]],
        drawOrder           = 0,
        -- castshadow          = true,
      },
    },

    smokeandsparks = {
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      air        = true,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        airdrag             = 0.97,
        colormap            = [[0.5 0.5 0.5 0.1   0.5 0.5 0.5 0.1   0.5 0.5 0.5 0.1   0.5 0.5 0.5 0.1   0 0 0 0]],
        directional         = false,
        emitrot             = 0,
        emitrotspread       = 0,
        emitvector          = [[0,0,0]],
        gravity             = [[0,0,0]],
        numparticles        = 1,
        particlelife        = 25,
        particlelifespread  = 9,
        particlesize        = s.fireballSize + s.smokeExtra,
        particlesizespread  = 0,
        particlespeed       = 0,
        particlespeedspread = 0,
        rotParams           = [[-24 r48, -60 r120, -180 r360]],
        animParams          = [[8,8,30]], --[xTiles, yTiles, animLength in game frames]
        pos                 = [[0,0,0]],
        sizegrowth          = -0.5,
        sizemod             = 1,
        texture             = [[generated-smoke]],
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
        colormap            = [[0.5 0.5 0.5 0.1   0.5 0.5 0.5 0.1   0.5 0.5 0.5 0.1   0.5 0.5 0.5 0.1   0 0 0 0]],
        dir                = [[0, 1, 0]],
        --gravity            = [[0.0, 0.1, 0.0]],
        frontoffset        = 0,
        animParams1          = [[8,8,30]],  -- front texture (engine 2026.09: muzzle flames read animParams1/2, not animParams)
        animParams2          = [[8,8,30]],  -- side texture --[xTiles, yTiles, animLength in game frames]
        fronttexture       = [[generated-smoke]],
        length             = s.flareLength,
        sidetexture        = [[none]],
        size               = s.fireballSize + s.flareExtra,
        sizegrowth         = 0,
        ttl                = 25,
        pos                = [[0, 3, 0]],
        --rotParams          = [[-10 r20, -20 r40, -180 r360]],
        drawOrder          = 0,
      },
    },
  }
end

-- Build and return the final table.
-- Keys stay identical to the old per-color files: genericshellexplosion-<size>-<color>
local result = {}
for colorName, c in pairs(colors) do
  for sizeName, s in pairs(sizes) do
    result["genericshellexplosion-" .. sizeName .. "-" .. colorName] = makeExplosion(s, c)
  end
end
return result
