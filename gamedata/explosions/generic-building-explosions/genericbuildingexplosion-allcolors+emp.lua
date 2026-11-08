-- genericbuildingexplosion (all colors, normal + emp)
-- Programmatically generated: edit the tables below, not the output.

-- Per-color values. Add/remove a color here and the loop at the bottom
-- emits the full small/medium/large/huge set for it, in both normal and -emp variants.
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

-- Per-size scaling values. Everything that changes between small/medium/large/huge lives here.
-- TA:Recoil: resized to TA's buildings (Splinter Faction's values in the comments). Target: the fireball ends at
-- about the building's size (radius ~35 / 60 / 90 / 140 elmos for 2x2 / 4x4 / 6x6 / 8x8+ footprints), ring ~1.5x
-- ground glow ~1.4x (it lingers). SF's reached 85-285 (fireball), 100-600 (ring) and lit the ground out to 200-800.
local sizes = {
  small = {
    centerSizegrowth    = 2.5,  -- 5
    circlegrowth        = 0.25,  -- 0.5 (x 200 frames)
    waveSize            = 3,  -- 8
    waveSpeed           = 2,  -- 8
    flashsize           = 40,  -- 200
    outerSizegrowth     = 5,  -- 10
    spikeSpeed          = 6,  -- 12
    sparkSize           = 6,  -- 20
    sparkSpeed          = 14,  -- 48
    smokeSpread         = 0.3,  -- 0.5
    smokeArea           = 15,  -- 60 (puffs scattered +-)
    smokeSize           = 5,  -- 10
    smokeExpansion      = 0.2,  -- 0.6
    dirtParticles       = 6,  -- 8
    dirtSize            = 4,  -- 8
    dirtSizeSpread      = 2,  -- 4
    dirtSpeed           = 2.5,  -- 5
    dirtSpeedSpread     = 1.5,  -- 3
    dirtSizegrowth      = 0.6,  -- 1.5
    fireballSize        = 18,  -- 40
    fireballGrowth      = 0.5,  -- 1.5 (x 30 frames)
    flareLength         = 18,  -- 40
    stormBolts          = 8,  -- 30 (emp)
    stormRadius         = 40,  -- -100..200
  },
  medium = {
    centerSizegrowth    = 4,  -- 8
    circlegrowth        = 0.45,  -- 1
    waveSize            = 4,  -- 8
    waveSpeed           = 2.5,  -- 8
    flashsize           = 65,  -- 400
    outerSizegrowth     = 7.5,  -- 15
    spikeSpeed          = 8,  -- 16
    sparkSize           = 9,  -- 20
    sparkSpeed          = 22,  -- 48
    smokeSpread         = 0.5,  -- 1
    smokeArea           = 30,  -- 60
    smokeSize           = 7,  -- 10
    smokeExpansion      = 0.3,  -- 0.6
    dirtParticles       = 8,  -- 10
    dirtSize            = 5,  -- 10
    dirtSizeSpread      = 2.5,  -- 5
    dirtSpeed           = 3.5,  -- 7
    dirtSpeedSpread     = 1.5,  -- 3
    dirtSizegrowth      = 0.8,  -- 1.5
    fireballSize        = 30,  -- 80
    fireballGrowth      = 1.0,  -- 1.5
    flareLength         = 30,  -- 40
    stormBolts          = 14,  -- 30
    stormRadius         = 70,  -- -100..200
  },
  large = {
    centerSizegrowth    = 6,  -- 12
    circlegrowth        = 0.68,  -- 2
    waveSize            = 6,  -- 8
    waveSpeed           = 3,  -- 8
    flashsize           = 95,  -- 600
    outerSizegrowth     = 15,  -- 30
    spikeSpeed          = 10,  -- 20
    sparkSize           = 12,  -- 20
    sparkSpeed          = 30,  -- 48
    smokeSpread         = 1,  -- 2
    smokeArea           = 45,  -- 60
    smokeSize           = 9,  -- 10
    smokeExpansion      = 0.45,  -- 0.6
    dirtParticles       = 10,  -- 12
    dirtSize            = 6,  -- 12
    dirtSizeSpread      = 3,  -- 6
    dirtSpeed           = 5,  -- 10
    dirtSpeedSpread     = 2,  -- 4
    dirtSizegrowth      = 1.0,  -- 1.5
    fireballSize        = 50,  -- 160
    fireballGrowth      = 1.3,  -- 1.5
    flareLength         = 45,  -- 40
    stormBolts          = 20,  -- 30
    stormRadius         = 100,  -- -100..200
  },
  huge = {
    centerSizegrowth    = 9,  -- 18
    circlegrowth        = 1.05,  -- 3
    waveSize            = 8,  -- 8
    waveSpeed           = 4,  -- 8
    flashsize           = 145,  -- 800
    outerSizegrowth     = 20,  -- 40
    spikeSpeed          = 14,  -- 26
    sparkSize           = 16,  -- 20
    sparkSpeed          = 42,  -- 48
    smokeSpread         = 1.5,  -- 3
    smokeArea           = 70,  -- 60
    smokeSize           = 10,  -- 10
    smokeExpansion      = 0.6,  -- 0.6
    dirtParticles       = 12,  -- 14
    dirtSize            = 8,  -- 14
    dirtSizeSpread      = 4,  -- 7
    dirtSpeed           = 7,  -- 14
    dirtSpeedSpread     = 2,  -- 4
    dirtSizegrowth      = 1.2,  -- 1.5
    fireballSize        = 80,  -- 240
    fireballGrowth      = 2.0,  -- 1.5
    flareLength         = 70,  -- 40
    stormBolts          = 30,  -- 30
    stormRadius         = 150,  -- -100..200
  },
}

-- s = size params, c = color params, isEmp = emp variant flag.
-- isEmp drives the whole variant difference:
--   * electricstorm block is added only for emp
--   * kickedupwater block is added only for non-emp
--   * kickedupdirt swaps colormap/texture and gains water flags for emp
local function makeExplosion(s, c, isEmp)
  local t = {
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
        particlelife        = 200, -- same as groundflash ttl
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
      ttl           = 200,
      water         = true,
      underwater    = true,
      color = {
        [1] = c.groundRGB[1],
        [2] = c.groundRGB[2],
        [3] = c.groundRGB[3],
      },
    },

    smoke = {
      air        = true,
      count      = 8,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        agespeed      = 0.01,
        alwaysvisible = true,
        color         = 0.1,
        pos           = [[r-]] .. s.smokeArea .. [[ r]] .. s.smokeArea .. [[, 24, r-]] .. s.smokeArea .. [[ r]] .. s.smokeArea .. [[]],
        size          = s.smokeSize,
        sizeexpansion = s.smokeExpansion,
        -- SF: [[r-3 r<spread>]] drifted every puff one way; even spread around the blast instead
        speed         = [[-]] .. s.smokeSpread .. [[ r]] .. (2 * s.smokeSpread) .. [[, 0.1 r1, -]] .. s.smokeSpread .. [[ r]] .. (2 * s.smokeSpread),
        startsize     = s.smokeSize,
      },
    },

    kickedupdirt = {
      air        = true,
      class      = [[CSimpleParticleSystem]],
      count      = 1,
      ground     = true,
      water      = isEmp and true or nil,
      underwater = isEmp and true or nil,
      properties = {
        airdrag             = 0.87,
        alwaysvisible       = true,
        colormap            = isEmp and [[0.75 0.75 1 0.05  0 0 0 0.0]] or [[0.25 0.25 0.25 0.5  0 0 0 0.0]],
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
        texture             = isEmp and [[whitelightb]] or [[bigexplosmoke]],
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
        airdrag             = 0.9,
        alwaysvisible       = true,
        colormap            = [[0.7 0.8 0.9 0.03   0.9 0.5 0.2 0.01]],
        directional         = true,
        emitrot             = 45,
        emitrotspread       = 32,
        emitvector          = [[0, 1, 0]],
        gravity             = [[0, -0.01, 0]],
        numparticles        = 16,
        particlelife        = 10,
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
        texture       = c.outerTex,
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
        animParams          = [[7,7,40]], --[xTiles, yTiles, animLength in game frames]
        pos                 = [[0,0,0]],
        sizegrowth          = s.fireballGrowth,
        sizemod             = 1,
        texture             = [[generated-buildingexplosion-static]],
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

  if isEmp then
    -- emp-only: lightning bolts scattered around the impact
    t.electricstorm = {
      air        = true,
      class      = [[CExpGenSpawner]],
      count      = s.stormBolts,
      ground     = true,
      water      = true,
      underwater = true,
      properties = {
        delay              = [[10 r200]],
        explosiongenerator = [[custom:lightning_stormbolt]],
        pos                = [[-]] .. s.stormRadius .. [[ r]] .. (2 * s.stormRadius) .. [[, 1, -]] .. s.stormRadius .. [[ r]] .. (2 * s.stormRadius),
      },
    }
  else
    -- non-emp-only: water splash (emp uses the kickedupdirt water flags instead)
    t.kickedupwater = {
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
    }
  end

  return t
end

-- Build and return the final table.
-- Keys stay identical to the old per-color files:
--   genericbuildingexplosion-<size>-<color>       (normal)
--   genericbuildingexplosion-<size>-<color>-emp   (emp)
local result = {}
for colorName, c in pairs(colors) do
  for sizeName, s in pairs(sizes) do
    local base = "genericbuildingexplosion-" .. sizeName .. "-" .. colorName
    result[base]            = makeExplosion(s, c, false)
    result[base .. "-emp"]  = makeExplosion(s, c, true)
  end
end
return result
