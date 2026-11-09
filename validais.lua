--------------------------------------------------------------------------------
--
--  validais.lua: the AIs a lobby may offer for this game. Name patterns
--  (Lua string patterns are not used: only "*" wildcards, as the engine
--  matches them). The game's own Lua AIs are defined in LuaAI.lua and
--  implemented by luarules/gadgets/ai_simpleai.lua. The engine's native
--  AIs (BARb, CircuitAI) carry Beyond All Reason unit knowledge and do not
--  play Total Annihilation, so they are left out; NullAI does nothing,
--  which Sandbox covers.
--
--------------------------------------------------------------------------------

return {
	{
		name = 'AdaptiveAI',
		desc = 'Reads the game every 30 seconds and adjusts its difficulty to stay a step ahead of you',
	},
	{
		name = 'Simple*AI',
		desc = 'SimpleAI (expands, techs and attacks in waves) and SimpleDefenderAI (the same, army kept at home)',
	},
	{
		name = 'Sandbox',
		desc = 'Does absolutely nothing',
	},
}
