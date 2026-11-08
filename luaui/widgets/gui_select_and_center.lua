-- From Splinter Faction (LuaUI/Widgets/gui_select_and_center.lua).
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

function widget:GetInfo()
    return {
        name    = "Select n Center!",
        desc    = "Selects and centers the Commander when it spawns.",
        author  = "quantum and Evil4Zerggin",
        date    = "19 April 2008",
        license = "GNU GPL, v2 or later",
        layer   = 5,
        enabled = true,
    }
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

function widget:Update()
    -- Remove immediately if spectating
    local _, _, spectator = Spring.GetPlayerInfo(Spring.GetMyPlayerID())
    if spectator then
        widgetHandler:RemoveWidget()
        return
    end

    -- Wait until the game is running
    if Spring.GetGameFrame() == 0 then return end

    -- Wait until a unit exists for our team
    local units = Spring.GetTeamUnits(Spring.GetMyTeamID())
    if not units or not units[1] then return end

    -- Commander has spawned — center and select
    local x, y, z = Spring.GetUnitPosition(units[1])
    -- TA:Recoil: SetCameraTarget centres in whichever camera mode the player uses (SF set the "spring" camera's
    -- state, which switched camera mode)
    Spring.SetCameraTarget(x, y, z, 0.5)
    Spring.SelectUnitArray({ units[1] })

    widgetHandler:RemoveWidget()
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------