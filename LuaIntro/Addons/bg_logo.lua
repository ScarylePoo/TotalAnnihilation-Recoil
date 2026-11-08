-- Shadows the engine base content's spinning Spring logo (LuaIntro/Addons/bg_logo.lua): TA:Recoil doesn't show it.
if addon.InGetInfo then
	return { name = "SpringLogo", desc = "disabled", author = "", date = "", license = "GPL2", layer = 1,
		enabled = false }
end
