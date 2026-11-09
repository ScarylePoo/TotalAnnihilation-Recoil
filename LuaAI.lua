--------------------------------------------------------------------------------
--
--  LuaAI.lua: the Lua AIs this game offers (luarules/gadgets/ai_simpleai.lua).
--
--------------------------------------------------------------------------------

return {
	{
		name = 'AdaptiveAI',
		desc = 'Adjusts its difficulty in real time to be a good match for you',
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
