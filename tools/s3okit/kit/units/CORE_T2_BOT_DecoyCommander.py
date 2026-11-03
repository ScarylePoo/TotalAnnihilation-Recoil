"""Decoy Commander (CORE_T2_BOT_DecoyCommander) - must pass for the real commander (that is the point of a decoy), so this spec
IS CORE_Commander's: same geometry, materials and hazard block, loaded from units/CORE_Commander.py so they cannot drift
apart. The piece layouts match (checked: same model/offsets). Script: scripts/CORE_T2_BOT_DecoyCommander.lua."""
import importlib.util, os

_s = importlib.util.spec_from_file_location('spec_CORE_Commander', os.path.join(os.path.dirname(__file__), 'CORE_Commander.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
UNIT = _m.UNIT
build = _m.build
