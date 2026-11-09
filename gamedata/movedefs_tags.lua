-- Defaults for movement-class tags a class in movedefs_classes.lua leaves out (gamedata/movedefs.lua), and the
-- tags movedefs_post.lua keeps consistent between a unit and its class. From Splinter Faction, except:
--   (slopeMod 4 as in SF: replaces the engine's default of 4 / maxSlope, ~10x stronger, so tanks and kbots slow
--   down much less on hills; user decision.)
--   footprintX/Z (2026-11-09): back in, as in SF: a unit's footprint is its movement class's (classes are sized to
--     their largest model, movedefs_classes.lua). Until then units kept TA's own footprints.
return {
	footprintX    = 1,
	footprintZ    = 1,
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
