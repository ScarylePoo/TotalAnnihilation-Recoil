if addon.InGetInfo then
	return {
		name    = "Music",
		desc    = "Plays the loading screen track; the in-game player (Slate Music) carries on with it, then the playlist",
		author  = "jK, Damgam; Splinter Faction; Scary le Poo",
		date    = "2012, 2013, 2023, 2026",
		license = "GPL2",
		layer   = 0,
		enabled = true,
	}
end

-- The track is LuaIntro/Configs/loadscreen.lua's music (TA's "Intro"); if it is missing, a random track from the
-- music library (music/<artist>/). At the player's music volume (snd_volmusic, Slate Music's setting, 20% if unset).
-- The track is left in the config value music_loadscreen_track, so Slate Music knows what is playing when the game
-- starts: it lets it finish and goes on to the next song. Off when music_loadscreen is 0.
function addon.Initialize()
	if Spring.GetConfigInt("music_loadscreen", 1) ~= 1 then
		Spring.SetConfigString("music_loadscreen_track", "")
		return
	end
	local ok, cfg = pcall(VFS.Include, "LuaIntro/Configs/loadscreen.lua")
	local pick = ok and type(cfg) == "table" and cfg.music
	if not (pick and VFS.FileExists(pick)) then
		local tracks = {}
		for _, dir in ipairs(VFS.SubDirs("music/", "*") or {}) do
			for _, path in ipairs(VFS.DirList(dir, "*.{ogg,mp3}") or {}) do
				tracks[#tracks + 1] = path
			end
		end
		if #tracks == 0 then
			Spring.SetConfigString("music_loadscreen_track", "")
			return
		end
		math.randomseed(os.clock() * 1000)
		pick = tracks[math.random(#tracks)]
	end
	local volume = math.max(0, math.min(100, Spring.GetConfigInt("snd_volmusic", 20))) * 0.01
	Spring.PlaySoundStream(pick, volume)
	Spring.SetSoundStreamVolume(volume)
	Spring.SetConfigString("music_loadscreen_track", pick)
end
