--------------------------------------------------------------------------------
--
--  LuaAI.lua: the Lua AIs this game offers (luarules/gadgets/ai_simpleai.lua).
--
--------------------------------------------------------------------------------

return {
	{
		name = 'AdaptiveAI',
		desc = 'Reads the game every 30 seconds and adjusts its difficulty to stay a step ahead of you',
	},
	{
		name = 'SimpleAI',
		desc = 'A straightforward opponent: expands, techs and attacks in waves',
	},
	{
		name = 'SimpleDefenderAI',
		desc = 'SimpleAI that keeps its army at home',
	},
	{
		name = 'Sandbox',
		desc = 'Does absolutely nothing',
	},
}
