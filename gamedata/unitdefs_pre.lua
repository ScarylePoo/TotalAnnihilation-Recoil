--------------------------------------------------------------------------------
-- Build lists
--
-- Builders use them as  buildoptions = Shared.buildList<Name>,  in their
-- units/*.lua (as Splinter Faction does). The lists are BOTA's original
-- [CANBUILD] lists from sidedata.tdf, in their original order, assembled from
-- the groups below.
--------------------------------------------------------------------------------

-- concatenates any number of lists into a new one
local function Join(...)
	local out = {}
	for i = 1, select('#', ...) do
		local list = select(i, ...)
		for j = 1, #list do
			out[#out + 1] = list[j]
		end
	end
	return out
end

--------------------------------------------------------------------------------
-- ARM
--------------------------------------------------------------------------------

local armT1Eco = {
	[[ARM_T1_ECO_SolarCollector]],
	[[ARM_T1_ECO_WindGenerator]],
	[[ARM_T1_ECO_EnergyStorage]],
	[[ARM_T1_ECO_MetalStorage]],
	[[ARM_T1_ECO_MetalExtractor]],
	[[ARM_T1_ECO_MetalMaker]],
}

local armT1Base = {
	[[ARM_T1_LAB_KbotLab]],
	[[ARM_T1_LAB_VehiclePlant]],
	[[ARM_T1_LAB_AircraftPlant]],
	[[ARM_T1_LAB_Shipyard]],
	[[ARM_T1_DEF_LLT]],
	[[ARM_T1_DEF_RadarTower]],
}

local armT1Defence = {
	[[ARM_T1_ECO_GeothermalPowerplant]],
	[[ARM_T1_DEF_Sentinel]],
	[[ARM_T1_DEF_Defender]],
	[[ARM_T1_DEF_DragonsTeeth]],
	[[ARM_T1_DEF_Guardian]],
}

local armT1SeaEco = {
	[[ARM_T1_SEADEF_SonarStation]],
	[[ARM_T1_SEAECO_TidalGenerator]],
	[[ARM_T1_SEAECO_UWEnergyStorage]],
	[[ARM_T1_SEAECO_UWMetalStorage]],
	[[ARM_T1_SEAECO_UWMetalExtractor]],
	[[ARM_T1_SEAECO_FloatingMetalMaker]],
}

local armT1SeaDefence = {
	[[ARM_T1_SEADEF_Defender]],
	[[ARM_T1_SEADEF_FloatingDragonsTeeth]],
	[[ARM_T1_SEADEF_Stingray]],
	[[ARM_T1_SEADEF_TorpedoLauncher]],
}

local armT2Tech = {
	[[ARM_T2_DEF_AdvancedRadar]],
	[[ARM_T2_ECO_FusionPowerplant]],
	[[ARM_T2_ECO_CloakableFusion]],
	[[ARM_T2_ECO_MohoMetalMaker]],
	[[ARM_T2_ECO_MohoMine]],
	[[ARM_T2_DEF_FortificationWall]],
	[[ARM_T2_DEF_Flakker]],
	[[ARM_T2_DEF_Ambusher]],
	[[ARM_T2_DEF_Annihilator]],
	[[ARM_T2_DEF_BigBertha]],
	[[ARM_T2_DEF_Protector]],
	[[ARM_T2_DEF_Retaliator]],
	[[ARM_T2_DEF_Stunner]],
	[[ARM_T2_DEF_Vulcan]],
	[[ARM_T2_DEF_AirRepairPad]],
	[[ARM_T2_DEF_TargetingFacility]],
}

-- constructors

Shared.buildListArmCommander = Join(armT1Eco, armT1Base,
	{ [[ARM_T1_DEF_DragonsTeeth]] },
	armT1SeaEco,
	{ [[ARM_T1_SEADEF_TorpedoLauncher]] })

Shared.buildListArmT1KbotConstructor = Join(armT1Eco, armT1Base,
	{ [[ARM_T2_LAB_AdvancedKbotLab]] },
	armT1Defence,
	{ [[ARM_T1_LAB_HovercraftPlatform]] })

Shared.buildListArmT1VehicleConstructor = Join(armT1Eco, armT1Base,
	{ [[ARM_T2_LAB_AdvancedVehiclePlant]] },
	armT1Defence,
	{ [[ARM_T1_LAB_HovercraftPlatform]] })

Shared.buildListArmT1AircraftConstructor = Join(armT1Eco, armT1Base,
	{ [[ARM_T2_LAB_AdvancedAircraftPlant]] },
	armT1Defence,
	{ [[ARM_T1_LAB_HovercraftPlatform]] })

-- hovercraft and seaplane constructors build the same things
Shared.buildListArmT1AmphibiousConstructor = Join(armT1Eco, armT1Base, armT1Defence, armT1SeaEco, armT1SeaDefence,
	{ [[ARM_T1_LAB_HovercraftPlatform]] })

Shared.buildListArmT1SeaConstructor = Join(
	{ [[ARM_T2_LAB_AdvancedShipyard]], [[ARM_T1_LAB_SeaplanePlatform]] },
	armT1SeaEco, armT1SeaDefence)

Shared.buildListArmT2KbotConstructor     = Join({ [[ARM_T1_LAB_KbotLab]] },      armT2Tech)
Shared.buildListArmT2VehicleConstructor  = Join({ [[ARM_T1_LAB_VehiclePlant]] }, armT2Tech)
Shared.buildListArmT2AircraftConstructor = Join({ [[ARM_T1_LAB_AircraftPlant]] }, armT2Tech)

Shared.buildListArmT2SeaConstructor = {
	[[ARM_T1_LAB_Shipyard]],
	[[ARM_T2_SEADEF_AdvancedSonar]],
	[[ARM_T2_SEAECO_UWFusionPowerplant]],
	[[ARM_T2_SEADEF_AdvancedTorpedoLauncher]],
}

Shared.buildListArmMineLayer = {
	[[ARM_T1_DEF_Mine1]],
	[[ARM_T1_DEF_Mine2]],
	[[ARM_T1_DEF_Mine3]],
	[[ARM_T1_DEF_Mine4]],
	[[ARM_T1_DEF_Mine5]],
	[[ARM_T1_DEF_Mine6]],
}

-- factories

Shared.buildListArmKbotLab = {
	[[ARM_T1_BOT_Constructor]],
	[[ARM_T1_BOT_Flea]],
	[[ARM_T1_BOT_Peewee]],
	[[ARM_T1_BOT_Rocko]],
	[[ARM_T1_BOT_Hammer]],
	[[ARM_T1_BOT_Jethro]],
	[[ARM_T1_BOT_Warrior]],
}

Shared.buildListArmVehiclePlant = {
	[[ARM_T1_VEH_Constructor]],
	[[ARM_T1_VEH_Jeffy]],
	[[ARM_T1_VEH_Flash]],
	[[ARM_T1_VEH_Stumpy]],
	[[ARM_T1_VEH_Samson]],
	[[ARM_T1_VEH_Podger]],
}

Shared.buildListArmAircraftPlant = {
	[[ARM_T1_AIR_Constructor]],
	[[ARM_T1_AIR_Peeper]],
	[[ARM_T1_AIR_FreedomFighter]],
	[[ARM_T1_AIR_Thunder]],
	[[ARM_T1_AIR_Atlas]],
}

Shared.buildListArmShipyard = {
	[[ARM_T1_SEA_Constructor]],
	[[ARM_T1_SEA_Skeeter]],
	[[ARM_T1_SEA_Crusader]],
	[[ARM_T1_SEA_Hulk]],
	[[ARM_T1_SEA_Lurker]],
}

Shared.buildListArmHovercraftPlatform = {
	[[ARM_T1_HOV_Constructor]],
	[[ARM_T1_HOV_Skimmer]],
	[[ARM_T1_HOV_Anaconda]],
	[[ARM_T1_HOV_Swatter]],
	[[ARM_T1_HOV_Wombat]],
	[[ARM_T1_HOV_Bear]],
}

Shared.buildListArmSeaplanePlatform = {
	[[ARM_T1_SEAPL_Constructor]],
	[[ARM_T2_AIR_Seahawk]],
	[[ARM_T1_AIR_FreedomFighter]],
	[[ARM_T1_SEAPL_Tornado]],
	[[ARM_T2_AIR_Lancet]],
	[[ARM_T1_SEAPL_Albatross]],
}

Shared.buildListArmAdvancedKbotLab = {
	[[ARM_T2_BOT_AdvancedConstructor]],
	[[ARM_T2_BOT_Marky]],
	[[ARM_T2_BOT_Eraser]],
	[[ARM_T2_BOT_Zipper]],
	[[ARM_T2_BOT_Zeus]],
	[[ARM_T2_BOT_Fido]],
	[[ARM_T2_BOT_Maverick]],
	[[ARM_T2_BOT_Pelican]],
	[[ARM_T2_BOT_Shooter]],
	[[ARM_T2_BOT_Invader]],
	[[ARM_T2_BOT_Infiltrator]],
	[[ARM_T2_BOT_FARK]],
	[[ARM_T2_BOT_DecoyCommander]],
}

Shared.buildListArmAdvancedVehiclePlant = {
	[[ARM_T2_VEH_AdvancedConstructor]],
	[[ARM_T2_VEH_Seer]],
	[[ARM_T2_VEH_Jammer]],
	[[ARM_T2_VEH_Panther]],
	[[ARM_T2_VEH_Bulldog]],
	[[ARM_T2_VEH_Luger]],
	[[ARM_T2_VEH_Merl]],
	[[ARM_T2_VEH_Phalanx]],
	[[ARM_T2_VEH_Penetrator]],
	[[ARM_T2_VEH_Triton]],
	[[ARM_T2_VEH_Spider]],
	[[ARM_T2_VEH_Scarab]],
}

Shared.buildListArmAdvancedAircraftPlant = {
	[[ARM_T2_AIR_AdvancedConstructor]],
	[[ARM_T2_AIR_Brawler]],
	[[ARM_T2_AIR_Phoenix]],
	[[ARM_T2_AIR_Hawk]],
	[[ARM_T2_AIR_Lancet]],
	[[ARM_T2_AIR_Eagle]],
	[[ARM_T2_AIR_Seahawk]],
}

Shared.buildListArmAdvancedShipyard = {
	[[ARM_T2_SEA_AdvancedConstructor]],
	[[ARM_T2_SEA_Colossus]],
	[[ARM_T2_SEA_Escort]],
	[[ARM_T2_SEA_Fibber]],
	[[ARM_T2_SEA_Archer]],
	[[ARM_T2_SEA_Piranha]],
	[[ARM_T2_SEA_Ranger]],
	[[ARM_T2_SEA_Conqueror]],
	[[ARM_T2_SEA_Millenium]],
}

--------------------------------------------------------------------------------
-- CORE
--------------------------------------------------------------------------------

local coreT1Eco = {
	[[CORE_T1_ECO_SolarCollector]],
	[[CORE_T1_ECO_WindGenerator]],
	[[CORE_T1_ECO_EnergyStorage]],
	[[CORE_T1_ECO_MetalStorage]],
	[[CORE_T1_ECO_MetalExtractor]],
	[[CORE_T1_ECO_MetalMaker]],
}

local coreT1Base = {
	[[CORE_T1_LAB_KbotLab]],
	[[CORE_T1_LAB_VehiclePlant]],
	[[CORE_T1_LAB_AircraftPlant]],
	[[CORE_T1_LAB_Shipyard]],
	[[CORE_T1_DEF_LightLaserTower]],
	[[CORE_T1_DEF_RadarTower]],
}

local coreT1Defence = {
	[[CORE_T1_ECO_GeothermalPowerplant]],
	[[CORE_T1_DEF_GaatGun]],
	[[CORE_T1_DEF_Pulverizer]],
	[[CORE_T1_DEF_DragonsTeeth]],
	[[CORE_T1_DEF_Punisher]],
}

local coreT1SeaEco = {
	[[CORE_T1_SEADEF_SonarStation]],
	[[CORE_T1_SEAECO_TidalGenerator]],
	[[CORE_T1_SEAECO_UWEnergyStorage]],
	[[CORE_T1_SEAECO_UWMetalStorage]],
	[[CORE_T1_SEAECO_UWMetalExtractor]],
	[[CORE_T1_SEAECO_FloatingMetalMaker]],
}

local coreT1SeaDefence = {
	[[CORE_T1_SEADEF_Stinger]],
	[[CORE_T1_SEADEF_FloatingDragonsTeeth]],
	[[CORE_T1_SEADEF_Thunderbolt]],
	[[CORE_T1_SEADEF_TorpedoLauncher]],
}

local coreT2Tech = {
	[[CORE_T2_DEF_AdvancedRadar]],
	[[CORE_T2_ECO_FusionPowerplant]],
	[[CORE_T2_ECO_CloakableFusion]],
	[[CORE_T2_ECO_MohoMetalMaker]],
	[[CORE_T2_ECO_MohoMine]],
	[[CORE_T2_DEF_FortificationWall]],
	[[CORE_T2_DEF_Cobra]],
	[[CORE_T2_DEF_Toaster]],
	[[CORE_T2_DEF_DoomsdayMachine]],
	[[CORE_T2_DEF_Intimidator]],
	[[CORE_T2_DEF_FortitudeMissileDefense]],
	[[CORE_T2_DEF_Silencer]],
	[[CORE_T2_DEF_Neutron]],
	[[CORE_T2_DEF_Buzzsaw]],
	[[CORE_T2_DEF_AirRepairPad]],
	[[CORE_T2_DEF_TargetingFacility]],
}

-- constructors

Shared.buildListCoreCommander = Join(coreT1Eco, coreT1Base, {
	[[CORE_T1_SEADEF_SonarStation]],
	[[CORE_T1_SEADEF_TorpedoLauncher]],
	[[CORE_T1_SEAECO_TidalGenerator]],
	[[CORE_T1_SEAECO_UWEnergyStorage]],
	[[CORE_T1_SEAECO_UWMetalStorage]],
	[[CORE_T1_SEAECO_UWMetalExtractor]],
	[[CORE_T1_SEAECO_FloatingMetalMaker]],
	[[CORE_T1_DEF_Immolator]],
	[[CORE_T1_DEF_DragonsTeeth]],
})

Shared.buildListCoreT1KbotConstructor = Join(coreT1Eco, coreT1Base,
	{ [[CORE_T2_LAB_AdvancedKbotLab]] },
	coreT1Defence,
	{ [[CORE_T1_LAB_HovercraftPlatform]], [[CORE_T1_DEF_Viper]], [[CORE_T1_DEF_Immolator]] })

Shared.buildListCoreT1VehicleConstructor = Join(coreT1Eco, coreT1Base,
	{ [[CORE_T2_LAB_AdvancedVehiclePlant]] },
	coreT1Defence,
	{ [[CORE_T1_LAB_HovercraftPlatform]], [[CORE_T1_DEF_Viper]], [[CORE_T1_DEF_Immolator]] })

Shared.buildListCoreT1AircraftConstructor = Join(coreT1Eco, coreT1Base,
	{ [[CORE_T2_LAB_AdvancedAircraftPlant]] },
	coreT1Defence,
	{ [[CORE_T1_LAB_HovercraftPlatform]], [[CORE_T1_DEF_Viper]], [[CORE_T1_DEF_Immolator]] })

Shared.buildListCoreT1HovercraftConstructor = Join(coreT1Eco, coreT1Base, coreT1Defence, coreT1SeaEco, coreT1SeaDefence,
	{ [[CORE_T1_LAB_HovercraftPlatform]], [[CORE_T1_DEF_Viper]], [[CORE_T1_DEF_Immolator]] })

-- as the hovercraft constructor, without the Immolator
Shared.buildListCoreT1SeaplaneConstructor = Join(coreT1Eco, coreT1Base, coreT1Defence, coreT1SeaEco, coreT1SeaDefence,
	{ [[CORE_T1_LAB_HovercraftPlatform]], [[CORE_T1_DEF_Viper]] })

Shared.buildListCoreT1SeaConstructor = {
	[[CORE_T2_LAB_AdvancedShipyard]],
	[[CORE_T1_LAB_SeaplanePlatform]],
	[[CORE_T1_SEADEF_TorpedoLauncher]],
	[[CORE_T1_SEAECO_TidalGenerator]],
	[[CORE_T1_SEADEF_SonarStation]],
	[[CORE_T1_SEAECO_UWEnergyStorage]],
	[[CORE_T1_SEAECO_UWMetalStorage]],
	[[CORE_T1_SEAECO_UWMetalExtractor]],
	[[CORE_T1_SEAECO_FloatingMetalMaker]],
	[[CORE_T1_SEADEF_Stinger]],
	[[CORE_T1_SEADEF_FloatingDragonsTeeth]],
	[[CORE_T1_SEADEF_Thunderbolt]],
}

-- only the kbot one builds the Krogoth Gantry
Shared.buildListCoreT2KbotConstructor     = Join({ [[CORE_T1_LAB_KbotLab]] }, coreT2Tech, { [[CORE_T3_LAB_KrogothGantry]] })
Shared.buildListCoreT2VehicleConstructor  = Join({ [[CORE_T1_LAB_VehiclePlant]] },  coreT2Tech)
Shared.buildListCoreT2AircraftConstructor = Join({ [[CORE_T1_LAB_AircraftPlant]] }, coreT2Tech)

Shared.buildListCoreT2SeaConstructor = {
	[[CORE_T1_LAB_Shipyard]],
	[[CORE_T2_SEADEF_AdvancedSonar]],
	[[CORE_T2_SEAECO_UWFusionPowerplant]],
	[[CORE_T2_SEADEF_AdvancedTorpedoLauncher]],
}

Shared.buildListCoreMineLayer = {
	[[CORE_T1_DEF_Mine1]],
	[[CORE_T1_DEF_Mine2]],
	[[CORE_T1_DEF_Mine3]],
	[[CORE_T1_DEF_Mine4]],
	[[CORE_T1_DEF_Mine5]],
	[[CORE_T1_DEF_Mine6]],
}

-- factories

Shared.buildListCoreKbotLab = {
	[[CORE_T1_BOT_Constructor]],
	[[CORE_T1_BOT_Ak]],
	[[CORE_T1_BOT_Storm]],
	[[CORE_T1_BOT_Thud]],
	[[CORE_T1_BOT_Crasher]],
}

Shared.buildListCoreVehiclePlant = {
	[[CORE_T1_VEH_Constructor]],
	[[CORE_T1_VEH_Weasel]],
	[[CORE_T1_VEH_Instigator]],
	[[CORE_T1_VEH_Raider]],
	[[CORE_T1_VEH_Slasher]],
	[[CORE_T1_VEH_Leveler]],
	[[CORE_T1_VEH_Spoiler]],
}

Shared.buildListCoreAircraftPlant = {
	[[CORE_T1_AIR_Constructor]],
	[[CORE_T1_AIR_Fink]],
	[[CORE_T1_AIR_Avenger]],
	[[CORE_T1_AIR_Shadow]],
	[[CORE_T1_AIR_Valkyrie]],
}

Shared.buildListCoreShipyard = {
	[[CORE_T1_SEA_Constructor]],
	[[CORE_T1_SEA_Searcher]],
	[[CORE_T1_SEA_Enforcer]],
	[[CORE_T1_SEA_Envoy]],
	[[CORE_T1_SEA_Snake]],
}

Shared.buildListCoreHovercraftPlatform = {
	[[CORE_T1_HOV_Constructor]],
	[[CORE_T1_HOV_Scrubber]],
	[[CORE_T1_HOV_Snapper]],
	[[CORE_T1_HOV_Slinger]],
	[[CORE_T1_HOV_Nixer]],
	[[CORE_T1_HOV_Turtle]],
}

Shared.buildListCoreSeaplanePlatform = {
	[[CORE_T1_SEAPL_Constructor]],
	[[CORE_T2_AIR_Hunter]],
	[[CORE_T1_AIR_Avenger]],
	[[CORE_T1_SEAPL_Voodoo]],
	[[CORE_T2_AIR_Titan]],
	[[CORE_T1_SEAPL_Typhoon]],
}

Shared.buildListCoreAdvancedKbotLab = {
	[[CORE_T2_BOT_AdvancedConstructor]],
	[[CORE_T2_BOT_Voyeur]],
	[[CORE_T2_BOT_Spectre]],
	[[CORE_T2_BOT_Freaker]],
	[[CORE_T2_BOT_Pyro]],
	[[CORE_T2_BOT_Morty]],
	[[CORE_T2_BOT_Gimp]],
	[[CORE_T2_BOT_Dominator]],
	[[CORE_T2_BOT_TheCan]],
	[[CORE_T2_BOT_Sumo]],
	[[CORE_T2_BOT_Roach]],
	[[CORE_T2_BOT_Necro]],
	[[CORE_T2_BOT_Parasite]],
	[[CORE_T2_BOT_DecoyCommander]],
}

Shared.buildListCoreAdvancedVehiclePlant = {
	[[CORE_T2_VEH_AdvancedConstructor]],
	[[CORE_T2_VEH_Informer]],
	[[CORE_T2_VEH_Deleter]],
	[[CORE_T2_VEH_Crock]],
	[[CORE_T2_VEH_Reaper]],
	[[CORE_T2_VEH_Goliath]],
	[[CORE_T2_VEH_Pillager]],
	[[CORE_T2_VEH_Diplomat]],
	[[CORE_T2_VEH_Copperhead]],
	[[CORE_T2_VEH_Hedgehog]],
}

Shared.buildListCoreAdvancedAircraftPlant = {
	[[CORE_T2_AIR_AdvancedConstructor]],
	[[CORE_T2_AIR_Rapier]],
	[[CORE_T2_AIR_Hurricane]],
	[[CORE_T2_AIR_Vamp]],
	[[CORE_T2_AIR_Titan]],
	[[CORE_T2_AIR_Hunter]],
	[[CORE_T2_AIR_Vulture]],
}

Shared.buildListCoreAdvancedShipyard = {
	[[CORE_T2_SEA_AdvancedConstructor]],
	[[CORE_T2_SEA_Hive]],
	[[CORE_T2_SEA_Phantom]],
	[[CORE_T2_SEA_Executioner]],
	[[CORE_T2_SEA_Warlord]],
	[[CORE_T2_SEA_MissileFrigate]],
	[[CORE_T2_SEA_Shredder]],
	[[CORE_T2_SEA_Shark]],
	[[CORE_T2_SEA_Leviathan]],
}

Shared.buildListCoreKrogothGantry = {
	[[CORE_T3_BOT_Krogoth]],
}

--------------------------------------------------------------------------------
-- unitdef names are lowercase; the engine checks build options against them
for _, list in pairs(Shared) do
	for i = 1, #list do
		list[i] = list[i]:lower()
	end
end
