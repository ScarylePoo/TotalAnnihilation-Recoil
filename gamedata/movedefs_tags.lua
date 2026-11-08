-- Defaults for movement-class tags a class in movedefs_classes.lua leaves out (gamedata/movedefs.lua), and the
-- tags movedefs_post.lua keeps consistent between a unit and its class. From Splinter Faction, except:
--   (slopeMod 4 as in SF: replaces the engine's default of 4 / maxSlope, ~10x stronger, so tanks and kbots slow
--   down much less on hills; user decision.)
--   footprintX/Z: not here, so units keep their own footprint (the remodels' build grid; e.g. the Krogoth is 3x3
--     in a 6x6 class) and missing ones still default to 1 in the engine.
return {
	crushStrength = 10,
	minWaterDepth = 10,
	maxWaterDepth = 0,
	subMarine     = 0,
	maxSlope      = 60,
	depthMod      = 0.1,
	slopeMod      = 4.0,
	heatMapping   = 1,
	heatMod       = 50,
	heatProduced  = 60,
}
