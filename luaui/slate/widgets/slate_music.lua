-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Music",
		desc    = "Plays the soundtrack by artist, shuffled, with random silences; controls in the game menu and options",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = -3,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  Music player. Plays the tracks under <dir>/<artist>/ for each folder in
--  MUSIC_DIRS, in a shuffled order that gets through every track before
--  repeating, with a random stretch of silence between some of them. No war
--  meters, no mood folders: one playlist, chosen by artist (or all of them).
--
--  Volume: snd_volmusic, 20% by default, applied to every track as it starts
--  (and to a track the loading screen left running, which this widget lets
--  finish rather than cutting off).
--
--  Controls live in the game menu (now playing, previous, pause, next) and in
--  Options > Sound. Other widgets use WG.SlateMusic:
--    GetStatus()  -> {title, artist, playing, paused, silent}
--    Previous(), Next(), TogglePause(), Play()
--    GetArtists() -> list of {folder, name}; GetArtist(), SetArtist(folder or "")
--    SetMusicVolume(percent)
--
--  No RmlUi document: this widget has nothing to draw.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- config
--------------------------------------------------------------------------------

-- Where the tracks are: each folder is scanned for <artist>/ subfolders, and
-- loose files straight in it count as one artist, "Various". A game keeps its
-- music in whichever of these it likes.
local MUSIC_DIRS  = { "music", "sounds/music" }
local EXTENSIONS  = "{*.ogg,*.mp3}"
local DEFAULT_VOLUME = 20       -- percent, snd_volmusic when unset

-- config keys (shared with the options)
local CFG_ARTIST       = "music_artist"            -- folder name, "" for all
local DEFAULT_ARTIST   = ""                        -- when nothing is chosen yet: all
local CFG_SILENCE_MAX  = "music_silence_max"       -- seconds, 0 for none
local CFG_SILENCE      = "UseSoundtrackSilenceTimer"
local CFG_FADES        = "UseSoundtrackFades"

local SILENCE_CHANCE  = 0.5     -- a gap after a track is a silence this often
local SILENCE_MIN     = 8       -- a silence is at least this long (seconds)
local GAP_TIME        = 1.5     -- the pause between tracks that is not a silence
local FADE_OUT_TIME   = 0.7     -- seconds, when skipping or pausing
local FADE_IN_TIME    = 1.2     -- seconds, as a track starts
local END_SLACK       = 0.5     -- a track this close to its end counts as over

--------------------------------------------------------------------------------
-- state
--------------------------------------------------------------------------------

local spGetConfigInt    = Spring.GetConfigInt
local spSetConfigInt    = Spring.SetConfigInt
local spGetConfigString = Spring.GetConfigString
local spSetConfigString = Spring.SetConfigString
local spPlayStream      = Spring.PlaySoundStream
local spStopStream      = Spring.StopSoundStream
local spPauseStream     = Spring.PauseSoundStream
local spSetStreamVolume = Spring.SetSoundStreamVolume
local spGetStreamTime   = Spring.GetSoundStreamTime
local spEcho            = Spring.Echo

local artists = {}       -- {folder, name, tracks = {paths}}
local artistByFolder = {}
local selectedArtist = "" -- folder, or "" for all

local bag = {}           -- tracks still to play this round
local history = {}       -- tracks played, newest last, for Previous
local HISTORY_MAX = 20

local current = nil      -- {path, title, artist}
local playing = false    -- a stream is running (or paused)
local paused = false
local silentUntil = nil  -- os.clock() when the next track may start
local fade = nil         -- {from, to, t, time, then = fn}
local volumeScale = 1    -- 0..1 from the fade

math.randomseed(os.clock() * 1000)

--------------------------------------------------------------------------------
-- the library
--------------------------------------------------------------------------------

-- "stormfront-clash" -> "Stormfront Clash"; "Xtadeus - Spe Noctis" stays
local function TitleOf(path, artistName)
	local file = path:match("[^/\\]+$") or path
	local title = file:gsub("%.[^.]+$", "")
	-- strip a leading "Artist - " the file name already carries
	local stripped = title:gsub("^" .. artistName:gsub("%p", "%%%1") .. "%s*%-%s*", "")
	if stripped ~= "" then title = stripped end
	if not title:find(" ") then
		title = title:gsub("[-_]+", " ")
	end
	title = title:gsub("(%a)([%w']*)", function(a, b) return a:upper() .. b end)
	return title
end

-- an artist folder may name itself in artist.txt
local function ArtistName(dir, folder)
	local custom = dir .. "/" .. folder .. "/artist.txt"
	if VFS.FileExists(custom) then
		local name = (VFS.LoadFile(custom) or ""):match("^%s*(.-)%s*$")
		if name ~= "" then return name end
	end
	return (folder:gsub("^%l", string.upper))
end

-- The same folder name under two music dirs is one artist. The key is the
-- folder name, so the saved choice (CFG_ARTIST) does not depend on the dir.
local function AddTracks(folder, name, tracks)
	local entry = artistByFolder[folder]
	if not entry then
		entry = { folder = folder, name = name, tracks = {} }
		artists[#artists + 1] = entry
		artistByFolder[folder] = entry
	end
	for _, t in ipairs(tracks) do
		entry.tracks[#entry.tracks + 1] = t
	end
end

local function Scan()
	artists, artistByFolder = {}, {}
	for _, dir in ipairs(MUSIC_DIRS) do
		for _, sub in ipairs(VFS.SubDirs(dir .. "/", "*") or {}) do
			local folder = sub:gsub("[/\\]+$", ""):match("[^/\\]+$")
			if folder then
				local tracks = VFS.DirList(dir .. "/" .. folder, EXTENSIONS) or {}
				if #tracks > 0 then
					AddTracks(folder, ArtistName(dir, folder), tracks)
				end
			end
		end
		-- loose files straight in the dir count as one unnamed artist
		local loose = VFS.DirList(dir, EXTENSIONS) or {}
		if #loose > 0 then
			AddTracks(".", "Various", loose)
		end
	end
	for _, a in ipairs(artists) do
		table.sort(a.tracks)
	end
	table.sort(artists, function(a, b) return a.name < b.name end)
end

local function Pool()
	local pool = {}
	if selectedArtist ~= "" and artistByFolder[selectedArtist] then
		local a = artistByFolder[selectedArtist]
		for _, t in ipairs(a.tracks) do pool[#pool + 1] = { path = t, artist = a } end
	else
		for _, a in ipairs(artists) do
			for _, t in ipairs(a.tracks) do pool[#pool + 1] = { path = t, artist = a } end
		end
	end
	return pool
end

-- refill the bag with every track of the selection, shuffled, the current
-- track kept out of the first draw
local function Refill()
	bag = Pool()
	for i = #bag, 2, -1 do
		local j = math.random(i)
		bag[i], bag[j] = bag[j], bag[i]
	end
	if current and #bag > 1 and bag[#bag].path == current.path then
		bag[#bag], bag[1] = bag[1], bag[#bag]
	end
end

local function Draw()
	if #bag == 0 then Refill() end
	if #bag == 0 then return nil end
	local t = table.remove(bag)
	return { path = t.path, artist = t.artist.name, title = TitleOf(t.path, t.artist.name) }
end

--------------------------------------------------------------------------------
-- playing
--------------------------------------------------------------------------------

local function Volume()
	return math.max(0, math.min(100, spGetConfigInt("snd_volmusic", DEFAULT_VOLUME))) * 0.01
end

local function ApplyVolume()
	spSetStreamVolume(Volume() * volumeScale)
end

local function FadesEnabled()
	return spGetConfigInt(CFG_FADES, 1) == 1
end

local function StartFade(from, to, time, after)
	if not FadesEnabled() or time <= 0 then
		volumeScale = to
		ApplyVolume()
		if after then after() end
		return
	end
	fade = { from = from, to = to, t = 0, time = time, after = after }
	volumeScale = from
	ApplyVolume()
end

local function PushHistory(track)
	history[#history + 1] = track
	if #history > HISTORY_MAX then
		table.remove(history, 1)
	end
end

local function StartTrack(track, fadeIn)
	if not track then
		playing = false
		current = nil
		return
	end
	current = track
	paused = false
	playing = true
	silentUntil = nil
	fade = nil
	-- the stream's own volume argument and the stream volume both, so the
	-- first second is never at full engine volume
	local v = Volume()
	spPlayStream(track.path, v)
	if fadeIn then
		StartFade(0, 1, FADE_IN_TIME)
	else
		volumeScale = 1
		ApplyVolume()
	end
	PushHistory(track)
end

local function Next(fromUser)
	local track = Draw()
	if playing and not paused and fromUser then
		StartFade(volumeScale, 0, FADE_OUT_TIME, function()
			spStopStream()
			StartTrack(track, true)
		end)
	else
		spStopStream()
		StartTrack(track, true)
	end
end

local function Previous()
	-- the one before the current, if there is one; else restart the current
	local target
	if #history >= 2 then
		table.remove(history) -- the current
		target = table.remove(history)
	elseif #history == 1 then
		target = table.remove(history)
	end
	if not target then
		return
	end
	StartFade(volumeScale, 0, playing and FADE_OUT_TIME or 0, function()
		spStopStream()
		StartTrack(target, true)
	end)
end

local function TogglePause()
	if not playing then
		-- in a gap or silence: play now
		Next(false)
		return
	end
	if paused then
		paused = false
		spPauseStream()
		StartFade(0, 1, FADE_IN_TIME * 0.5)
	else
		StartFade(volumeScale, 0, FADE_OUT_TIME, function()
			spPauseStream()
			paused = true
		end)
	end
end

-- the gap after a track: a silence some of the time, a short pause otherwise
local function ScheduleGap()
	local maxSilence = spGetConfigInt(CFG_SILENCE_MAX, 60)
	local gap = GAP_TIME
	if spGetConfigInt(CFG_SILENCE, 1) == 1 and maxSilence > 0 and math.random() < SILENCE_CHANCE then
		gap = math.random(math.min(SILENCE_MIN, maxSilence), maxSilence)
	end
	silentUntil = os.clock() + gap
	playing = false
end

--------------------------------------------------------------------------------
-- widget api
--------------------------------------------------------------------------------

function widget:Initialize()
	Scan()
	if #artists == 0 then
		spEcho("[Slate Music] no tracks under " .. table.concat(MUSIC_DIRS, "/ or ") .. "/, removing widget")
		widgetHandler:RemoveWidget(self)
		return
	end
	selectedArtist = spGetConfigString(CFG_ARTIST, DEFAULT_ARTIST)
	if selectedArtist ~= "" and not artistByFolder[selectedArtist] then
		selectedArtist = ""
	end
	Refill()

	-- The loading screen may have left a stream running: let it finish at the
	-- user's volume. Its file is not known here, so it is not put in the
	-- history (Previous cannot go back to it) and the playlist starts after it.
	local played, total = spGetStreamTime()
	if total and total > 0 and played and played < total - END_SLACK then
		current = { artist = "", title = "Loading screen music" }
		playing = true
		paused = false
		volumeScale = 1
		ApplyVolume()
	else
		StartTrack(Draw(), true)
	end

	WG.SlateMusic = {
		GetStatus = function()
			return {
				title   = current and current.title or "",
				artist  = current and current.artist or "",
				playing = playing,
				paused  = paused,
				silent  = (not playing) and silentUntil ~= nil,
			}
		end,
		Next       = function() Next(true) end,
		Previous   = Previous,
		TogglePause = TogglePause,
		Play       = function() if not playing or paused then TogglePause() end end,
		GetArtists = function()
			local list = {}
			for _, a in ipairs(artists) do list[#list + 1] = { folder = a.folder, name = a.name, count = #a.tracks } end
			return list
		end,
		GetArtist  = function() return selectedArtist end,
		SetArtist  = function(folder)
			folder = folder or ""
			if folder ~= "" and not artistByFolder[folder] then folder = "" end
			if folder == selectedArtist then return end
			selectedArtist = folder
			spSetConfigString(CFG_ARTIST, folder)
			Refill()
			-- the current track may belong to another artist: move on
			if current and folder ~= "" and current.artist ~= artistByFolder[folder].name then
				Next(true)
			end
		end,
		SetMusicVolume = function(percent)
			spSetConfigInt("snd_volmusic", math.floor(percent + 0.5))
			ApplyVolume()
		end,
	}
end

function widget:Shutdown()
	WG.SlateMusic = nil
end

function widget:Update(dt)
	-- fades
	if fade then
		fade.t = fade.t + dt
		local k = math.min(1, fade.t / fade.time)
		volumeScale = fade.from + (fade.to - fade.from) * k
		ApplyVolume()
		if k >= 1 then
			local after = fade.after
			fade = nil
			if after then after() end
		end
		return
	end
	-- the track ended?
	if playing and not paused then
		local played, total = spGetStreamTime()
		if not total or total <= 0 or (played and played >= total - END_SLACK) then
			ScheduleGap()
		end
	end
	-- the gap is over?
	if not playing and silentUntil and os.clock() >= silentUntil then
		StartTrack(Draw(), true)
	end
end
