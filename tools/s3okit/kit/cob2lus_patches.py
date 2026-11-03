"""Deliberate changes on top of what cob2lus.py generates, applied to the generated text. A patch that no longer matches stops the unit (loud, not silently lost).

PITCH: direct-fire guns whose COB ignored pitch (found with AIM=1 run.sh, flag NOPITCH): the user wants guns to point at their targets, fidelity to OTA does not matter.
RESTORE: TargetCleared was the COB's only way back, and the engine never calls it, so these guns froze where they last aimed."""


def _pitch(aim_turn, wait, piece, speed, restore_turn):
    return [(aim_turn, f'{aim_turn}\n\tTurn({piece}, x_axis, -pitch, rad({speed}))'),
            (wait, f'{wait}\n\tWaitForTurn({piece}, x_axis)'),
            (restore_turn, f'{restore_turn}\n\tTurn({piece}, x_axis, 0, rad({speed}))')]


def _restore(aim_end, pieces):
    """a restore thread ahead of Create, started at the end of the aim; pieces: (piece, axis, deg/s)"""
    turns = '\n'.join(f'\tTurn({p}, {a}, 0, rad({s}))' for p, a, s in pieces)
    return [('function script.Create()', f'local function RestoreAfterDelay()\n\tSleep(5000)\n{turns}\nend\n\nfunction script.Create()'),
            (aim_end, aim_end.replace('\treturn true', '\tStartThread(RestoreAfterDelay)\n\treturn true'))]


PATCHES = {
    'CORE_T1_VEH_Instigator': _pitch('\tTurn(turret, y_axis, heading, rad(180))', '\tWaitForTurn(turret, y_axis)\n\tStartThread(RestoreAfterDelay, 2000)'.split('\n')[0],
                                     'sleeve', 90, '\tTurn(turret, y_axis, 0, rad(90))'),
    'CORE_T1_VEH_Weasel': _pitch('\tTurn(turret, y_axis, heading, rad(199.95))', '\tWaitForTurn(turret, y_axis)', 'barrel', 90, '\tTurn(turret, y_axis, 0, rad(89.98))'),
    'CORE_T2_SEA_Warlord': _pitch('\tTurn(turreta, y_axis, heading, rad(200))', '\tWaitForTurn(turreta, y_axis)', 'guna', 60, '\tTurn(turreta, y_axis, 0, rad(100))'),
    'ARM_T2_DEF_Vulcan': _restore('\tWaitForTurn(neck, x_axis)\n\tSleep(115)\n\treturn true', [('turret', 'y_axis', 5), ('neck', 'x_axis', 2)]),
    'CORE_T2_DEF_Intimidator': _restore('\tWaitForTurn(gun, x_axis)\n\treturn true', [('turret', 'y_axis', 5), ('gun', 'x_axis', 2)]),
}


def apply(stem, body):
    for old, new in PATCHES.get(stem, ()):
        if body.count(old) != 1:
            raise ValueError(f'{stem}: patch does not match exactly once: {old!r}')
        body = body.replace(old, new)
    return body
